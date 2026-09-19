import json

from datetime import timedelta

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models import (
    ApprovalRequest,
    User,
    Membership,
)

from app.agent.executor import execute_plan

from app.logs.audit_logger import audit_log


# =========================================================
# CREATE APPROVAL REQUEST
# =========================================================


def create_approval_request(
    vendor_id: int | None,
    plan: dict
):
    
    print("VENDOR:", vendor_id)
    print("PLAN:", plan)

    db: Session = SessionLocal()

    try:

        action = plan.get(
            "tool",
            "unknown"
        )

        preview = None


        # -------------------------------------------------
        # VALIDATE + GENERATE ACTION PREVIEW
        # -------------------------------------------------

        if action == "extend_trial":

            query = plan.get(
                "query",
                {}
            )


            # Validate query

            if not isinstance(
                query,
                dict
            ):

                return {
                    "error":
                    "Invalid action data"
                }


            # Get user identifier

            user_identifier = (
                query.get("user")
                or query.get("crm_id")
            )


            if not user_identifier:

                return {
                    "error":
                    "User identifier missing"
                }


            # Validate extension days

            try:

                days = int(
                    query.get(
                        "days",
                        7
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                return {
                    "error":
                    "Invalid number of days"
                }


            if days <= 0:

                return {
                    "error":
                    "Extension days must be greater than 0"
                }


            # -------------------------------------------------
            # FIND USER
            # -------------------------------------------------

            user_query = db.query(
                User
            )


            # Vendor isolation

            if vendor_id is not None:

                   user_query = user_query.filter(
        User.vendor_id == vendor_id
    )

            user = user_query.filter(

                (
                    User.crm_id.ilike(
                        f"%{user_identifier}%"
                    )
                )

                |

                (
                    User.name.ilike(
                        f"%{user_identifier}%"
                    )
                )

            ).first()


            # -------------------------------------------------
            # VALIDATE USER
            # -------------------------------------------------

            if user is None:

                return {

                    "error":
                    f"User {user_identifier} not found"

                }


            # -------------------------------------------------
            # FIND MEMBERSHIP
            # -------------------------------------------------

            membership = db.query(
                Membership
            ).filter(

                Membership.user_id
                ==
                user.id

            ).first()


            # -------------------------------------------------
            # VALIDATE MEMBERSHIP
            # -------------------------------------------------

            if membership is None:

                return {

                    "error":
                    (
                        "Membership not found for "
                        f"{user.crm_id}"
                    )

                }


            if membership.end_date is None:

                return {

                    "error":
                    "Membership expiry date unavailable"

                }


            # -------------------------------------------------
            # CALCULATE NEW EXPIRY DATE
            # -------------------------------------------------

            current_end_date = (
                membership.end_date
            )


            new_end_date = (

                current_end_date

                +

                timedelta(
                    days=days
                )

            )


            # -------------------------------------------------
            # GENERATE PREVIEW
            # -------------------------------------------------

            preview = {

                "user":
                user.name,

                "crm_id":
                user.crm_id,

                "days":
                days,

                "current_end_date":
                str(
                    current_end_date
                ),

                "new_end_date":
                str(
                    new_end_date
                ),

            }


        # -------------------------------------------------
        # CREATE APPROVAL REQUEST
        # -------------------------------------------------

        approval = ApprovalRequest(

            vendor_id=vendor_id,

            action=action,

            plan=json.dumps(
                plan,
                default=str
            ),

            status="pending"

        )


        db.add(
            approval
        )


        db.commit()


        db.refresh(
            approval
        )


        # -------------------------------------------------
        # AUDIT LOG
        # -------------------------------------------------

        audit_log(

            "APPROVAL_CREATED",

            {

                "approval_id":
                approval.id,

                "vendor_id":
                vendor_id,

                "action":
                action,

                "preview":
                preview,

            }

        )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "id":
            approval.id,

            "vendor_id":
            approval.vendor_id,

            "action":
            approval.action,

            "status":
            approval.status,

            "created_at":
            approval.created_at,

            "preview":
            preview,

        }


    except Exception:

        db.rollback()

        raise


    finally:

        db.close()


# =========================================================
# GET APPROVAL REQUEST
# =========================================================


def get_approval_request(
    approval_id: int
):

    db: Session = SessionLocal()

    try:

        approval = (

            db.query(
                ApprovalRequest
            )

            .filter(

                ApprovalRequest.id
                ==
                approval_id

            )

            .first()

        )


        if approval is None:

            return None


        return {

            "id":
            approval.id,

            "vendor_id":
            approval.vendor_id,

            "action":
            approval.action,

            "status":
            approval.status,

            "plan":
            json.loads(
                approval.plan
            ),

            "created_at":
            approval.created_at,

        }


    finally:

        db.close()


# =========================================================
# APPROVE REQUEST
# =========================================================


def approve_request(
    approval_id: int
):

    db: Session = SessionLocal()

    try:

        approval = (

            db.query(
                ApprovalRequest
            )

            .filter(

                ApprovalRequest.id
                ==
                approval_id

            )

            .first()

        )


        # -------------------------------------------------
        # VALIDATE APPROVAL
        # -------------------------------------------------

        if approval is None:

            return {

                "error":
                "Approval request not found"

            }


        if approval.status != "pending":

            return {

                "error":
                (
                    "Approval already "
                    f"{approval.status}"
                )

            }


        # -------------------------------------------------
        # LOAD STORED PLAN
        # -------------------------------------------------

        plan = json.loads(
            approval.plan
        )


        # -------------------------------------------------
        # EXECUTE ACTION
        # -------------------------------------------------

        execution_result = execute_plan(
    plan=plan,
    vendor_id=approval.vendor_id,
)


        # -------------------------------------------------
        # HANDLE EXECUTION ERROR
        # -------------------------------------------------

        if execution_result.get(
            "error"
        ):

            db.rollback()

            return {

                "error":
                execution_result["error"]

            }


        # -------------------------------------------------
        # UPDATE APPROVAL STATUS
        # -------------------------------------------------

        approval.status = "approved"


        db.commit()


        db.refresh(
            approval
        )


        # -------------------------------------------------
        # AUDIT LOG
        # -------------------------------------------------

        audit_log(

            "APPROVAL_APPROVED",

            {

                "approval_id":
                approval.id,

                "execution_result":
                execution_result,

            }

        )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "id":
            approval.id,

            "status":
            approval.status,

            "execution_result":
            execution_result,

        }


    except Exception:

        db.rollback()

        raise


    finally:

        db.close()


# =========================================================
# REJECT REQUEST
# =========================================================


def reject_request(
    approval_id: int
):

    db: Session = SessionLocal()

    try:

        approval = (

            db.query(
                ApprovalRequest
            )

            .filter(

                ApprovalRequest.id
                ==
                approval_id

            )

            .first()

        )


        # -------------------------------------------------
        # VALIDATE APPROVAL
        # -------------------------------------------------

        if approval is None:

            return {

                "error":
                "Approval request not found"

            }


        if approval.status != "pending":

            return {

                "error":
                (
                    "Approval already "
                    f"{approval.status}"
                )

            }


        # -------------------------------------------------
        # REJECT REQUEST
        # -------------------------------------------------

        approval.status = "rejected"


        db.commit()


        db.refresh(
            approval
        )


        # -------------------------------------------------
        # AUDIT LOG
        # -------------------------------------------------

        audit_log(

            "APPROVAL_REJECTED",

            {

                "approval_id":
                approval.id,

                "action":
                approval.action,

            }

        )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "id":
            approval.id,

            "status":
            approval.status,

            "message":
            "Action rejected",

        }


    except Exception:

        db.rollback()

        raise


    finally:

        db.close()


# =========================================================
# LIST PENDING REQUESTS
# =========================================================


def list_pending_requests(
    vendor_id: int
):

    db: Session = SessionLocal()

    try:

        approvals = (

            db.query(
                ApprovalRequest
            )

            .filter(

                ApprovalRequest.vendor_id
                ==
                vendor_id,

                ApprovalRequest.status
                ==
                "pending",

            )

            .all()

        )


        return [

            {

                "id":
                approval.id,

                "vendor_id":
                approval.vendor_id,

                "action":
                approval.action,

                "status":
                approval.status,

                "created_at":
                approval.created_at,

            }

            for approval in approvals

        ]


    finally:

        db.close()