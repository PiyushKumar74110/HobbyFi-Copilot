from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from datetime import datetime

from app.database import Base


class Vendor(Base):

    __tablename__ = "vendors"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    # NEW
    password_hash = Column(
        String,
        nullable=False
    )

    # NEW
    role = Column(
        String,
        default="vendor",
        nullable=False
    )

    # NEW (optional but recommended)
    is_active = Column(
        Integer,
        default=1
    )

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    vendor_id = Column(
        Integer,
        ForeignKey("vendors.id")
    )

    name = Column(
        String
    )

    email = Column(
        String
    )

    phone = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    

    crm_id = Column(
    String,
    unique=True,
    nullable=True,
    index=True
)


class Membership(Base):

    __tablename__ = "memberships"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    plan = Column(
        String
    )

    status = Column(
        String
    )

    start_date = Column(
        DateTime
    )

    end_date = Column(
        DateTime
    )


class Payment(Base):

    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    amount = Column(
        Float
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ApprovalRequest(Base):

    __tablename__ = "approval_requests"

    id = Column(
        Integer,
        primary_key=True
    )

    vendor_id = Column(
        Integer
    )

    action = Column(
        String,
        nullable=False
    )

    # Stores the complete planner output
    plan = Column(
        Text,
        nullable=False
    )

    status = Column(
        String,
        default="pending",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    event = Column(
        String
    )

    details = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )