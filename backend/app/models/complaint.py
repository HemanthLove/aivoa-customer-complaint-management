from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    customer_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    customer_source: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    product_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    product_strength: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    batch_number: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    manufacturing_date: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    expiry_date: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    affected_quantity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    affected_quantity_unit: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    complaint_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    facility_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    material_impact: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    defect_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    defect_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    severity: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    risk_level: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    recommended_action: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    risk_rationale: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        default="text",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )