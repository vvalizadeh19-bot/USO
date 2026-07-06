"""Master Data Domain (§3.3) — reference data imported from / referenced by CPM.

Owner: Project Manager / Admin. Most records originate from CPM.
"""
from __future__ import annotations

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, PKMixin, SoftDeleteMixin, TimestampMixin


class Province(Base, PKMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "provinces"

    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    region: Mapped[str | None] = mapped_column(String(60), nullable=True)  # منطقه e.g. R9

    cities: Mapped[list["City"]] = relationship(back_populates="province")


class City(Base, PKMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "cities"
    __table_args__ = (UniqueConstraint("province_id", "name", name="uq_city_province"),)

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    province_id: Mapped[int] = mapped_column(ForeignKey("provinces.id"), nullable=False)

    province: Mapped[Province] = relationship(back_populates="cities")


class Contractor(Base, PKMixin, TimestampMixin, SoftDeleteMixin):
    """Drive-Test contractor company (§3.7). An Aggregate Root."""

    __tablename__ = "contractors"

    name: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    code: Mapped[str | None] = mapped_column(String(40), unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class ProblemCategory(Base, PKMixin, TimestampMixin, SoftDeleteMixin):
    """Admin-extensible Health Check problem categories (§2.8)."""

    __tablename__ = "problem_categories"

    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


DEFAULT_PROBLEM_CATEGORIES = [
    "Temporary Power",
    "NWG Responsibility",
    "MS Responsibility",
    "Project Responsibility",
]
