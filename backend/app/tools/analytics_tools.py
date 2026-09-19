from datetime import datetime, timedelta

from app.database import SessionLocal

from app.models import (
    User,
    Membership,
    Payment
)

from sqlalchemy import func


def total_users(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        count = (
            db.query(User)
            .filter(
                User.vendor_id == vendor_id
            )
            .count()
        )

        return {
            "total_users": count
        }

    finally:

        db.close()

def new_users_this_month(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        now = datetime.utcnow()

        start = datetime(
            now.year,
            now.month,
            1
        )


        count = (
            db.query(User)
            .filter(
                User.vendor_id == vendor_id,
                User.created_at >= start
            )
            .count()
        )


        return {

            "new_users_this_month":
            count

        }


    finally:

        db.close()

def active_memberships(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        count = (
            db.query(Membership)
            .join(
                User,
                Membership.user_id == User.id
            )
            .filter(
                User.vendor_id == vendor_id,
                Membership.status == "active"
            )
            .count()
        )


        return {

            "active_memberships":
            count

        }


    finally:

        db.close()

def expired_memberships(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        count = (
            db.query(Membership)
            .join(
                User,
                Membership.user_id == User.id
            )
            .filter(
                User.vendor_id == vendor_id,
                Membership.status == "expired"
            )
            .count()
        )


        return {

            "expired_memberships":
            count

        }


    finally:

        db.close()

def revenue_this_month(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        now = datetime.utcnow()

        start = datetime(
            now.year,
            now.month,
            1
        )


        revenue = (
            db.query(
                func.sum(Payment.amount)
            )
            .join(
                User,
                Payment.user_id == User.id
            )
            .filter(
                User.vendor_id == vendor_id,
                Payment.created_at >= start
            )
            .scalar()
        )


        return {

            "revenue_this_month":
            revenue or 0.0

        }


    finally:

        db.close()

def revenue_last_30_days(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        start = (
            datetime.utcnow()
            - timedelta(days=30)
        )


        revenue = (
            db.query(
                func.sum(Payment.amount)
            )
            .join(
                User,
                Payment.user_id == User.id
            )
            .filter(
                User.vendor_id == vendor_id,
                Payment.created_at >= start
            )
            .scalar()
        )


        return {

            "revenue_last_30_days":
            revenue or 0.0

        }


    finally:

        db.close()

def average_payment(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        avg = (
            db.query(
                func.avg(Payment.amount)
            )
            .join(
                User,
                Payment.user_id == User.id
            )
            .filter(
                User.vendor_id == vendor_id
            )
            .scalar()
        )


        return {

            "average_payment":
            round(avg or 0.0, 2)

        }


    finally:

        db.close()

def top_membership_plans(query: dict):

    vendor_id = query.get("vendor_id")

    limit = query.get(
        "limit",
        5
    )

    db = SessionLocal()

    try:

        plans = (
            db.query(
                Membership.plan,
                func.count(Membership.id).label("count")
            )
            .join(
                User,
                Membership.user_id == User.id
            )
            .filter(
                User.vendor_id == vendor_id
            )
            .group_by(
                Membership.plan
            )
            .order_by(
                func.count(Membership.id).desc()
            )
            .limit(
                limit
            )
            .all()
        )


        return [

            {
                "plan":
                plan,

                "count":
                count
            }

            for plan, count in plans

        ]


    finally:

        db.close()

def dashboard_summary(query: dict):

    total_users_result = total_users(query)
    new_users_result = new_users_this_month(query)
    active_memberships_result = active_memberships(query)
    expired_memberships_result = expired_memberships(query)
    revenue_this_month_result = revenue_this_month(query)
    revenue_last_30_days_result = revenue_last_30_days(query)
    average_payment_result = average_payment(query)
    top_plans_result = top_membership_plans(query)


    total_users_value = total_users_result.get(
        "total_users",
        0
    )

    new_users_value = new_users_result.get(
        "new_users_this_month",
        0
    )

    active_memberships_value = active_memberships_result.get(
        "active_memberships",
        0
    )

    expired_memberships_value = expired_memberships_result.get(
        "expired_memberships",
        0
    )

    revenue_month_value = revenue_this_month_result.get(
        "revenue_this_month",
        0
    )

    revenue_30_days_value = revenue_last_30_days_result.get(
        "revenue_last_30_days",
        0
    )

    average_payment_value = average_payment_result.get(
        "average_payment",
        0
    )


    top_plans_lines = []

    for item in top_plans_result:

        top_plans_lines.append(
            f"- {item['plan']}: {item['count']} users"
        )


    top_plans_text = "\n".join(
        top_plans_lines
    )


    return f"""
Dashboard Summary:

Total Users: {total_users_value}
New Users This Month: {new_users_value}
Active Memberships: {active_memberships_value}
Expired Memberships: {expired_memberships_value}

Revenue This Month: {revenue_month_value}
Revenue Last 30 Days: {revenue_30_days_value}
Average Payment: {average_payment_value}

Top Membership Plans:
{top_plans_text}
""".strip()