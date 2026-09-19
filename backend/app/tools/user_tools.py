from app.database import SessionLocal

from app.models import (
    User,
    Membership,
)

from sqlalchemy import or_




from app.models import (
    User,
    Membership,
)


def get_users_by_plan(query: dict):

    vendor_id = query.get("vendor_id")
    plan = query.get("query")


    if not plan:

        return {
            "error":
            "Please provide a membership plan."
        }


    db = SessionLocal()


    try:

        users = (
            db.query(
                User,
                Membership,
            )
            .join(
                Membership,
                Membership.user_id
                ==
                User.id,
            )
            .filter(
                Membership.plan.ilike(
                    f"%{plan}%"
                )
            )
            
        )

        if vendor_id is not None:

            users = users.filter(
                User.vendor_id == vendor_id
            )

        users = users.all()


        if not users:

            return {
                "message":
                f"No users found for plan '{plan}'."
            }


        return [

            {
                "crm_id":
                user.crm_id,

                "name":
                user.name,

                "email":
                user.email,

                "plan":
                membership.plan,

                "status":
                membership.status,
            }

            for user, membership in users
        ]


    finally:

        db.close()



def get_users(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()

    try:

        user_query = db.query(
            User
        )


        if vendor_id is not None:

            user_query = user_query.filter(
                User.vendor_id == vendor_id
            )


        users = user_query.all()


        return [

            {
                "id": user.id,
                "crm_id": user.crm_id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
            }

            for user in users

        ]


    finally:

        db.close()





def search_user(query: dict):

    vendor_id = query.get("vendor_id")
    name = query.get("query")

    if not name or not name.strip():

        return {

            "error":
            "Please provide user name or CRM ID."

        }


    db = SessionLocal()


    try:


        user_query = db.query(
            User
        )


        if vendor_id is not None:

            user_query = user_query.filter(
                User.vendor_id == vendor_id
            )



        # -------------------------
        # Exact CRM ID match first
        # -------------------------

        exact_user = user_query.filter(

            User.crm_id == name

        ).first()



        if exact_user:

            return {

                "id":
                exact_user.id,

                "crm_id":
                exact_user.crm_id,

                "name":
                exact_user.name,

                "email":
                exact_user.email,

                "phone":
                exact_user.phone,

            }



        # -------------------------
        # Partial search
        # -------------------------

        users = user_query.filter(

            or_(

                User.name.ilike(
                    f"%{name}%"
                ),

                User.crm_id.ilike(
                    f"%{name}%"
                )

            )

        ).all()



        if len(users) == 0:

            return {

                "message":
                f"No user found with '{name}'."

            }



        if len(users) > 1:

            return {

                "message":
                "Multiple users found. Please provide full CRM ID.",

                "users":[

                    {
                        "crm_id":u.crm_id,
                        "name":u.name
                    }

                    for u in users

                ]

            }



        user = users[0]


        return {

            "id":
            user.id,

            "crm_id":
            user.crm_id,

            "name":
            user.name,

            "email":
            user.email,

            "phone":
            user.phone,

        }



    finally:

        db.close()





def get_trial_users(query: dict):

    vendor_id = query.get("vendor_id")

    db = SessionLocal()


    try:


        user_query = (

            db.query(User)

            .join(
                Membership
            )

            .filter(
                Membership.status == "trial"
            )

        )



        if vendor_id is not None:

            user_query = user_query.filter(
                User.vendor_id == vendor_id
            )



        users = user_query.all()



        return [

            {

                "crm_id":
                user.crm_id,

                "name":
                user.name,

                "email":
                user.email

            }

            for user in users

        ]



    finally:

        db.close()









