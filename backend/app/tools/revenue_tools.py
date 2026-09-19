from datetime import datetime, timedelta


from app.database import SessionLocal

from app.models import Payment





def get_revenue(
    query: str = None
):

    db = SessionLocal()

    try:

        today = datetime.utcnow().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )


        payments = db.query(
            Payment
        ).filter(

            Payment.created_at >= today

        ).all()


        total = sum(

            payment.amount

            for payment in payments

        )



        return {

            "date":
            str(today),


            "total_revenue":
            total,


            "transactions":
            len(payments)

        }



    finally:

        db.close()

def get_revenue_by_date(
    days_ago:int=1
):

    db = SessionLocal()

    try:

        target_date = (
            datetime.utcnow().date()
            -
            timedelta(days=days_ago)
        )


        start = datetime.combine(
            target_date,
            datetime.min.time()
        )


        end = datetime.combine(
            target_date,
            datetime.max.time()
        )


        payments = db.query(
            Payment
        ).filter(
            Payment.created_at >= start,
            Payment.created_at <= end
        ).all()


        return {

            "date":str(target_date),

            "revenue":
            sum(
                p.amount
                for p in payments
            ),

            "transactions":
            len(payments)
        }


    finally:

        db.close()





def get_total_revenue(
    query: str = None
):


    db = SessionLocal()


    try:


        payments = db.query(
            Payment
        ).all()



        total = sum(

            payment.amount

            for payment in payments

        )



        return {

            "total_revenue":
            total,

            "transactions":
            len(payments)

        }



    finally:

        db.close()