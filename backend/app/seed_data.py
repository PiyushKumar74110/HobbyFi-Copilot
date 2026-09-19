from datetime import datetime, timedelta
from app.security.password import hash_password

import os
from app.config import settings

# print("Working Directory:", os.getcwd())
# print("Database URL:", settings.DATABASE_URL)
# print("Database File:", os.path.abspath("hobbyfi.db"))


from app.database import (
    Base,
    engine,
    SessionLocal,
)

from app.models import (
    Vendor,
    User,
    Membership,
    Payment,
)


Base.metadata.create_all(
    bind=engine
)


db = SessionLocal()


try:

    # ==========================================
    # Vendors
    # ==========================================

    badminton_vendor = Vendor(
    name="HobbyFi Badminton Academy",
    email="badminton@hobbyfi.com",
    password_hash=hash_password("badminton123"),
)

    cricket_vendor = Vendor(
    name="HobbyFi Cricket Academy",
    email="cricket@hobbyfi.com",
    password_hash=hash_password("cricket123"),
)

    fitness_vendor = Vendor(
    name="HobbyFi Fitness Center",
    email="fitness@hobbyfi.com",
    password_hash=hash_password("fitness123"),
)


    db.add_all([
        badminton_vendor,
        cricket_vendor,
        fitness_vendor,
    ])


    db.commit()


    db.refresh(badminton_vendor)
    db.refresh(cricket_vendor)
    db.refresh(fitness_vendor)


    # ==========================================
    # Users
    # ==========================================

    # --------------------------
    # Vendor 1 - Badminton
    # --------------------------

    rahul = User(
        vendor_id=badminton_vendor.id,
        name="Rahul",
        email="rahul@example.com",
        phone="9999999991",
    )

    priya = User(
        vendor_id=badminton_vendor.id,
        name="Priya",
        email="priya@example.com",
        phone="9999999992",
    )

    amit = User(
        vendor_id=badminton_vendor.id,
        name="Amit",
        email="amit@example.com",
        phone="9999999993",
    )

    sneha = User(
        vendor_id=badminton_vendor.id,
        name="Sneha",
        email="sneha@example.com",
        phone="9999999994",
    )


    # --------------------------
    # Vendor 2 - Cricket
    # --------------------------

    rohan = User(
        vendor_id=cricket_vendor.id,
        name="Rohan",
        email="rohan@example.com",
        phone="9999999995",
    )

    arjun = User(
        vendor_id=cricket_vendor.id,
        name="Arjun",
        email="arjun@example.com",
        phone="9999999996",
    )

    neha = User(
        vendor_id=cricket_vendor.id,
        name="Neha",
        email="neha@example.com",
        phone="9999999997",
    )


    # --------------------------
    # Vendor 3 - Fitness
    # --------------------------

    vikram = User(
        vendor_id=fitness_vendor.id,
        name="Vikram",
        email="vikram@example.com",
        phone="9999999998",
    )

    pooja = User(
        vendor_id=fitness_vendor.id,
        name="Pooja",
        email="pooja@example.com",
        phone="9999999999",
    )

    karan = User(
        vendor_id=fitness_vendor.id,
        name="Karan",
        email="karan@example.com",
        phone="9999999900",
    )


    users = [
        rahul,
        priya,
        amit,
        sneha,
        rohan,
        arjun,
        neha,
        vikram,
        pooja,
        karan,
    ]


    db.add_all(users)

    db.commit()


    for user in users:

        db.refresh(user)


    # ==========================================
    # Generate Vendor Scoped CRM IDs
    # ==========================================

    vendor_users = {

        badminton_vendor.id: [
            rahul,
            priya,
            amit,
            sneha,
        ],

        cricket_vendor.id: [
            rohan,
            arjun,
            neha,
        ],

        fitness_vendor.id: [
            vikram,
            pooja,
            karan,
        ],

    }


    for vendor_id, users_list in vendor_users.items():

        for index, user in enumerate(
            users_list,
            start=1,
        ):

            user.crm_id = (
                f"HF{vendor_id}{index:03d}"
            )


    db.commit()


    # ==========================================
    # Memberships
    # ==========================================

    memberships = [

        # Badminton

        Membership(
            user_id=rahul.id,
            plan="Badminton",
            status="trial",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow()
            + timedelta(days=7),
        ),

        Membership(
            user_id=priya.id,
            plan="Badminton Premium",
            status="active",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow()
            + timedelta(days=30),
        ),

        Membership(
            user_id=amit.id,
            plan="Badminton",
            status="expired",
            start_date=datetime.utcnow()
            - timedelta(days=60),
            end_date=datetime.utcnow()
            - timedelta(days=30),
        ),

        Membership(
            user_id=sneha.id,
            plan="Badminton Premium",
            status="trial",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow()
            + timedelta(days=10),
        ),


        # Cricket

        Membership(
            user_id=rohan.id,
            plan="Cricket",
            status="trial",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow()
            + timedelta(days=7),
        ),

        Membership(
            user_id=arjun.id,
            plan="Cricket Premium",
            status="active",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow()
            + timedelta(days=45),
        ),

        Membership(
            user_id=neha.id,
            plan="Cricket",
            status="active",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow()
            + timedelta(days=30),
        ),


        # Fitness

        Membership(
            user_id=vikram.id,
            plan="Fitness",
            status="trial",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow()
            + timedelta(days=14),
        ),

        Membership(
            user_id=pooja.id,
            plan="Fitness Premium",
            status="active",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow()
            + timedelta(days=60),
        ),

        Membership(
            user_id=karan.id,
            plan="Gym",
            status="expired",
            start_date=datetime.utcnow()
            - timedelta(days=90),
            end_date=datetime.utcnow()
            - timedelta(days=10),
        ),

    ]


    db.add_all(memberships)


    # ==========================================
    # Payments
    # ==========================================

    payments = [

        Payment(
            user_id=rahul.id,
            amount=500,
            created_at=datetime.utcnow(),
        ),

        Payment(
            user_id=priya.id,
            amount=1500,
            created_at=datetime.utcnow(),
        ),

        Payment(
            user_id=sneha.id,
            amount=800,
            created_at=datetime.utcnow()
            - timedelta(days=2),
        ),

        Payment(
            user_id=rohan.id,
            amount=700,
            created_at=datetime.utcnow(),
        ),

        Payment(
            user_id=arjun.id,
            amount=2000,
            created_at=datetime.utcnow()
            - timedelta(days=1),
        ),

        Payment(
            user_id=neha.id,
            amount=1200,
            created_at=datetime.utcnow()
            - timedelta(days=5),
        ),

        Payment(
            user_id=vikram.id,
            amount=600,
            created_at=datetime.utcnow(),
        ),

        Payment(
            user_id=pooja.id,
            amount=2500,
            created_at=datetime.utcnow()
            - timedelta(days=3),
        ),

        Payment(
            user_id=karan.id,
            amount=1000,
            created_at=datetime.utcnow()
            - timedelta(days=30),
        ),

    ]


    db.add_all(payments)

    db.commit()


    # ==========================================
    # Output
    # ==========================================

    print(
        "HobbyFi seed data created successfully."
    )


    print(
        "\nGenerated CRM IDs:"
    )


    for vendor_id, users_list in vendor_users.items():

        print(
            f"\nVendor {vendor_id}"
        )

        for user in users_list:

            print(
                f"{user.name} -> "
                f"{user.crm_id}"
            )


finally:

    db.close()

