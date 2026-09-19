from datetime import timedelta, datetime

from app.database import SessionLocal
from sqlalchemy.orm import Session


from app.models import (
    User,
    Membership
)



def find_user(
    db,
    identifier: str,
    vendor_id: int | None = None,
):
    print("find_user called")
    print("identifier =", identifier)
    print("vendor_id =", vendor_id)

    if not identifier:
        return None

    identifier = identifier.strip()

    db = SessionLocal()

    # -------------------------
    # CRM ID Search
    # -------------------------

    if identifier.upper().startswith("HF"):

        user_query = db.query(User).filter(
            User.crm_id.ilike(
                identifier.upper()
            )
        )
        
        if vendor_id is not None:
            user_query = user_query.filter(
                User.vendor_id == vendor_id
            )

        return user_query.first()

    # -------------------------
    # Name Search
    # -------------------------

    user_query = db.query(User).filter(
        User.name.ilike(f"%{identifier}%")
    )

    if vendor_id is not None:
        user_query = user_query.filter(
            User.vendor_id == vendor_id
        )

    users = user_query.all()

    if len(users) == 1:
        return users[0]

    if len(users) > 1:

        return {
            "multiple_users": True,
            "users": [
                {
                    "name": u.name,
                    "crm_id": u.crm_id,
                }
                for u in users
            ],
        }

    return None



# ==========================
# GET MEMBERSHIP
# ==========================


def get_membership(query: dict):

    db = SessionLocal()

    try:

        vendor_id = query.get("vendor_id")

        identifier = (
    query.get("user")
    or query.get("crm_id")
    or query.get("query")
)

        user = find_user(
            db,
            identifier,
            vendor_id,
        )

        if user is None:
            return {
                "error": "User not found"
            }

        if isinstance(user, dict):
            return user

        membership = (
            db.query(Membership)
            .filter(
                Membership.user_id == user.id
            )
            .first()
        )

        if membership is None:
            return {
                "error": "Membership not found"
            }

        return {
            "crm_id": user.crm_id,
            "user": user.name,
            "plan": membership.plan,
            "status": membership.status,
            "end_date": str(
                membership.end_date
            ),
        }

    finally:
        db.close()



# ==========================
# ACTIVE MEMBERSHIPS
# ==========================


def get_active_memberships(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        membership_query = (
            db.query(Membership, User)
            .join(
                User,
                Membership.user_id == User.id
            )
            .filter(
                Membership.status == "active"
            )
        )

        if vendor_id is not None:

            membership_query = membership_query.filter(
                User.vendor_id == vendor_id
            )

        rows = membership_query.all()

        return [

            {
                "crm_id": user.crm_id,
                "user": user.name,
                "plan": membership.plan,
                "end_date": str(
                    membership.end_date
                ),
            }

            for membership, user in rows

        ]

    finally:
        db.close()



# ==========================
# EXTEND MEMBERSHIP
# ==========================


def extend_membership(query: dict):

    db = SessionLocal()

    try:

        identifier = (
    query.get("user")
    or query.get("crm_id")
    or query.get("query")
)

        vendor_id = query.get("vendor_id")

        days = query.get(
            "days",
            7
        )

        if not identifier:

            return {
                "error":
                "User missing"
            }

        try:

            days = int(days)

        except ValueError:

            return {
                "error":
                "Days must be numeric"
            }

        # -------------------------
        # Find User
        # -------------------------

        user = find_user(
            db,
            identifier,
            vendor_id
        )

        if user is None:

            return {
                "error":
                "User not found"
            }

        if isinstance(user, dict):

            return user

        # -------------------------
        # Membership
        # -------------------------

        membership = (
            db.query(Membership)
            .filter(
                Membership.user_id == user.id
            )
            .first()
        )

        if membership is None:

            return {
                "error":
                "Membership not found"
            }

        old_end_date = membership.end_date

        # -------------------------
        # Business Logic
        # -------------------------

        if membership.status == "expired":

            membership.status = "active"

            membership.end_date = (
                datetime.utcnow()
                + timedelta(days=days)
            )

        else:

            membership.end_date = (
                membership.end_date
                + timedelta(days=days)
            )

        db.commit()

        db.refresh(membership)

        return {

            "message":
            "Membership extended successfully",

            "crm_id":
            user.crm_id,

            "user":
            user.name,

            "plan":
            membership.plan,

            "old_end_date":
            str(old_end_date),

            "new_end_date":
            str(membership.end_date),

            "status":
            membership.status

        }

    finally:

        db.close()

def extend_trial(query: dict):

    db = SessionLocal()

    try:

        vendor_id = query.get("vendor_id")

        user_identifier = (
    query.get("user")
    or query.get("crm_id")
    or query.get("query")
)

        days = query.get("days", 7)

        if not user_identifier:

            return {
                "error": "User missing"
            }

        try:
            days = int(days)
        except:
            return {
                "error": "Days must be numeric"
            }

        # -------------------------
        # Vendor Scoped User Search
        # -------------------------

        user = find_user(
            db=db,
            identifier=user_identifier,
            vendor_id=vendor_id,
        )

        if user is None:

            return {
                "error": "User not found"
            }

        # Multiple users returned

        if isinstance(user, dict):

            return user

        # -------------------------
        # Membership
        # -------------------------

        membership = (
            db.query(Membership)
            .filter(
                Membership.user_id == user.id
            )
            .first()
        )

        if membership is None:

            return {
                "error": "Membership not found"
            }

        old_end_date = membership.end_date

        # -------------------------
        # Business Logic
        # -------------------------

        if membership.status == "expired":

            membership.status = "active"

            membership.end_date = (
                datetime.utcnow()
                + timedelta(days=days)
            )

        else:

            membership.end_date = (
                membership.end_date
                + timedelta(days=days)
            )

        db.commit()

        db.refresh(membership)

        return {

            "message":
            "Membership extended successfully",

            "crm_id":
            user.crm_id,

            "user":
            user.name,

            "plan":
            membership.plan,

            "old_end_date":
            str(old_end_date),

            "new_end_date":
            str(membership.end_date),

            "status":
            membership.status,

        }

    finally:

        db.close()