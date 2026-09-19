from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Vendor

from app.security.password import verify_password
from app.security.auth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(request: LoginRequest):

    db: Session = SessionLocal()

    try:

        vendor = (

            db.query(Vendor)

            .filter(
                Vendor.email == request.email
            )

            .first()

        )

        if vendor is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not verify_password(
            request.password,
            vendor.password_hash
        ):

            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token(

            {
                "vendor_id": vendor.id
            }

        )

        return {

            "access_token": token,

            "token_type": "bearer",

            "vendor": {

                "id": vendor.id,

                "name": vendor.name,

                "email": vendor.email

            }

        }

    finally:

        db.close()