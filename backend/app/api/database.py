
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.database import engine
from app.models import (
    ApprovalRequest,
    AuditLog,
    Membership,
    Payment,
    User,
    Vendor,
)
from app.security.dependencies import get_current_vendor, get_db

router = APIRouter(
    prefix="/database",
    tags=["Database Explorer"],
)

# Only these tables are available through the explorer.
ALLOWED_TABLES = {
    "vendors",
    "users",
    "memberships",
    "payments",
    "approval_requests",
    "audit_logs",
}


def serialize_row(row, excluded_fields=None):
    """Convert a SQLAlchemy model instance into JSON-compatible fields."""
    excluded_fields = excluded_fields or set()
    result = {}

    for column in inspect(row).mapper.column_attrs:
        name = column.key

        if name in excluded_fields:
            continue

        value = getattr(row, name)
        result[name] = value.isoformat() if hasattr(value, "isoformat") else value

    return result


@router.get("/tables")
def list_tables(
    current_vendor=Depends(get_current_vendor),
):
    """List the database tables available in the explorer."""
    return {
        "tables": sorted(ALLOWED_TABLES),
    }


@router.get("/{table_name}")
def get_table_records(
    table_name: str,
    search: str = Query(default="", max_length=200),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_vendor=Depends(get_current_vendor),
    db: Session = Depends(get_db),
):
    """Return a paginated, vendor-scoped view of an allowed database table."""
    if table_name not in ALLOWED_TABLES:
        raise HTTPException(status_code=404, detail="Table not found")

    query = None
    excluded_fields = set()

    if table_name == "vendors":
        # A vendor can view only their own vendor record.
        query = db.query(Vendor).filter(Vendor.id == current_vendor.id)
        excluded_fields = {"password_hash"}

    elif table_name == "users":
        query = db.query(User).filter(User.vendor_id == current_vendor.id)

    elif table_name == "memberships":
        query = (
            db.query(Membership)
            .join(User, Membership.user_id == User.id)
            .filter(User.vendor_id == current_vendor.id)
        )

    elif table_name == "payments":
        query = (
            db.query(Payment)
            .join(User, Payment.user_id == User.id)
            .filter(User.vendor_id == current_vendor.id)
        )

    elif table_name == "approval_requests":
        query = db.query(ApprovalRequest).filter(
            ApprovalRequest.vendor_id == current_vendor.id
        )

    elif table_name == "audit_logs":
        # AuditLog has no vendor_id, so it cannot safely be exposed
        # as vendor-scoped until its ownership is established.
        raise HTTPException(
            status_code=403,
            detail="Audit logs are not available in the vendor explorer",
        )

    if search:
        searchable_columns = [
            column for column in query.column_descriptions[0]["entity"].__table__.columns
            if column.name not in excluded_fields
            and str(column.type).lower().find("text") == -1
            and str(column.type).lower().find("blob") == -1
        ]

        from sqlalchemy import cast, String, or_

        query = query.filter(
            or_(
                *[
                    cast(column, String).ilike(f"%{search}%")
                    for column in searchable_columns
                ]
            )
        )

    total = query.count()
    rows = query.order_by(query.column_descriptions[0]["entity"].id).offset(offset).limit(limit).all()

    return {
        "table": table_name,
        "total": total,
        "limit": limit,
        "offset": offset,
        "records": [
            serialize_row(row, excluded_fields)
            for row in rows
        ],
    }
