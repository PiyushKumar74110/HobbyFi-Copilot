
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Vendor
from app.security.password import verify_password
from app.security.auth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Authenticate a vendor and return an access token."""
    db: Session = SessionLocal()

    try:
        vendor = (
            db.query(Vendor)
            .filter(Vendor.email == form_data.username)
            .first()
        )

        if vendor is None or not verify_password(
            form_data.password,
            vendor.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        token = create_access_token(
            {"vendor_id": vendor.id}
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "vendor": {
                "id": vendor.id,
                "name": vendor.name,
                "email": vendor.email,
            },
        }

    finally:
        db.close()
