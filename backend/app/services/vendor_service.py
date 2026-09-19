from backend.app.models import Vendor
from app.database import SessionLocal



def get_vendor(
    vendor_id: int
):


    db = SessionLocal()


    try:

        vendor = db.query(
            Vendor
        ).filter(
            Vendor.id == vendor_id
        ).first()


        if not vendor:

            return None


        return {

            "id":
            vendor.id,

            "name":
            vendor.name,

            "email":
            vendor.email

        }


    finally:

        db.close()





def validate_vendor_access(
    vendor_id: int,
    resource_vendor_id: int
):


    return (
        vendor_id ==
        resource_vendor_id
    )