from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Vendor
from app.security.auth import (
    SECRET_KEY,
    ALGORITHM,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_vendor(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db),

):

    credentials_exception = HTTPException(

        status_code=401,

        detail="Invalid authentication credentials",

    )

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM],

        )

        vendor_id = payload.get("vendor_id")

        if vendor_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    vendor = (

        db.query(Vendor)

        .filter(Vendor.id == vendor_id)

        .first()

    )

    if vendor is None:
        raise credentials_exception

    return vendor