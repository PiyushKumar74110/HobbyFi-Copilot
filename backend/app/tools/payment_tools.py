from datetime import datetime

from app.database import SessionLocal

from app.models import (
    User,
    Payment
)

from sqlalchemy import func



def get_user_by_crm(
    db,
    crm_id,
    vendor_id
):

    return (
        db.query(User)
        .filter(
            User.crm_id == crm_id,
            User.vendor_id == vendor_id
        )
        .first()
    )



def create_payment(query: dict):

    vendor_id = query.get("vendor_id")
    crm_id = query.get("crm_id")
    amount = query.get("amount")


    if crm_id is None:
        return {
            "error":"crm_id is required"
        }

    if not crm_id.startswith("HF"):

        return {
        "error":"Invalid CRM ID format"
    }


    if amount is None:
        return {
            "error":"amount is required"
        }


    db = SessionLocal()

    try:

        user = get_user_by_crm(
            db,
            crm_id,
            vendor_id
        )


        if not user:
            return {
                "error":"User not found."
            }


        payment = Payment(
            user_id=user.id,
            amount=float(amount),
            created_at=datetime.utcnow()
        )


        db.add(payment)
        db.commit()
        db.refresh(payment)


        return {

            "payment_id": payment.id,
            "crm_id": user.crm_id,
            "amount": payment.amount,
            "created_at": str(payment.created_at)

        }


    finally:

        db.close()





def get_payment(query: dict):

    vendor_id = query.get("vendor_id")
    payment_id = query.get("payment_id")

    print("PAYMENT ID:", payment_id)
    print("VENDOR ID:", vendor_id)


    if payment_id is None:
        return {
            "error":"payment_id is required"
        }


    db = SessionLocal()

    try:


        payment = (
            db.query(Payment)
            .join(
                User,
                Payment.user_id == User.id
            )
            .filter(
                Payment.id == payment_id,
                User.vendor_id == vendor_id
            )
            .first()
        )


        if not payment:
            return {
                "error":"Payment not found."
            }


        user = (
    db.query(User)
    .filter(
        User.id == payment.user_id
    )
    .first()
)

        return {

    "payment_id": payment.id,
    "crm_id": user.crm_id if user else None,
    "amount": payment.amount,
    "created_at": str(payment.created_at)

}


    finally:

        db.close()






def list_payments(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        payments = (
            db.query(
                Payment,
                User.crm_id
            )
            .join(
                User,
                Payment.user_id == User.id
            )
            .filter(
                User.vendor_id == vendor_id
            )
            .order_by(
                Payment.created_at.desc()
            )
            .all()
        )


        return [

            {
                "payment_id": payment.id,
                "crm_id": crm_id,
                "amount": payment.amount,
                "created_at": str(payment.created_at)
            }

            for payment, crm_id in payments

        ]


    finally:

        db.close()





def list_user_payments(query: dict):

    vendor_id = query.get("vendor_id")
    crm_id = query.get("crm_id")


    if crm_id is None:

        return {
            "error":"crm_id is required"
        }


    db = SessionLocal()

    try:


        user = get_user_by_crm(
            db,
            crm_id,
            vendor_id
        )


        if not user:

            return {
                "error":"User not found."
            }



        payments = (
    db.query(Payment)
    .join(
        User,
        Payment.user_id == User.id
    )
    .filter(
        User.vendor_id == vendor_id,
        User.id == user.id
    )
    .order_by(
        Payment.created_at.desc()
    )
    .all()
)


        return [

            {
                "payment_id": payment.id,
                "crm_id": user.crm_id,
                "amount": payment.amount,
                "created_at": str(payment.created_at)
            }

            for payment in payments

        ]


    finally:

        db.close()






def update_payment_amount(query: dict):

    vendor_id = query.get("vendor_id")
    payment_id = query.get("payment_id")
    new_amount = query.get("new_amount")


    if payment_id is None:
        return {
            "error":"payment_id is required"
        }


    db = SessionLocal()

    try:


        payment = (
            db.query(Payment)
            .join(
                User,
                Payment.user_id == User.id
            )
            .filter(
                Payment.id == payment_id,
                User.vendor_id == vendor_id
            )
            .first()
        )


        if not payment:

            return {
                "error":"Payment not found."
            }



        payment.amount = float(new_amount)


        db.commit()
        db.refresh(payment)



        return {

            "message":"Payment updated successfully.",
            "payment_id":payment.id,
            "amount":payment.amount,
            "created_at":str(payment.created_at)

        }


    finally:

        db.close()






def delete_payment(query: dict):

    vendor_id = query.get("vendor_id")
    payment_id = query.get("payment_id")


    if payment_id is None:
        return {
            "error":"payment_id is required"
        }


    db = SessionLocal()

    try:


        payment = (
            db.query(Payment)
            .join(
                User,
                Payment.user_id == User.id
            )
            .filter(
                Payment.id == payment_id,
                User.vendor_id == vendor_id
            )
            .first()
        )


        if not payment:

            return {
                "error":"Payment not found."
            }


        db.delete(payment)
        db.commit()


        return {

            "message":"Payment deleted successfully.",
            "payment_id":payment_id

        }


    finally:

        db.close()






def total_revenue(query: dict):

    vendor_id = query.get("vendor_id")


    db = SessionLocal()

    try:


        total = (
            db.query(
                Payment
            )
            .join(
                User,
                Payment.user_id == User.id
            )
            .filter(
                User.vendor_id == vendor_id
            )
            .with_entities(
                func.sum(Payment.amount)
            )
            .scalar()
        )


        return {

            "total_revenue": total or 0

        }


    finally:

        db.close()






def latest_payment(query: dict):

    vendor_id = query.get("vendor_id")


    db = SessionLocal()

    try:


        payment = (
            db.query(Payment)
            .join(
                User,
                Payment.user_id == User.id
            )
            .filter(
                User.vendor_id == vendor_id
            )
            .order_by(
                Payment.created_at.desc()
            )
            .first()
        )


        if not payment:

            return {
                "message":"No payments found."
            }



        user = (
    db.query(User)
    .filter(
        User.id == payment.user_id
    )
    .first()
)

        return {

    "payment_id":payment.id,
    "crm_id":user.crm_id if user else None,
    "amount":payment.amount,
    "created_at":str(payment.created_at)

}

    finally:

        db.close()