"""Site — physical telecom location (§1.8).

A Site owns location/geography. Because ~half of CPM rows arrive with
``site_id = "No Site ID"`` (only a temporary code exists), the Site is keyed by
``site_code`` = the real Irancell Site ID when present, otherwise the temporary
code. When a real Site ID later replaces the temporary one, the CPM importer
raises a Change Request (§2.4) rather than silently overwriting.
"""
from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, PKMixin, SoftDeleteMixin, TimestampMixin

NO_SITE_ID = "No Site ID"


class Site(Base, PKMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "sites"

    # Business identity — the effective code used everywhere else.
    site_code: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    irancell_site_id: Mapped[str | None] = mapped_column(String(60), nullable=True, index=True)
    temp_site_id: Mapped[str | None] = mapped_column(String(60), nullable=True, index=True)
    is_temporary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    province_id: Mapped[int] = mapped_column(ForeignKey("provinces.id"), nullable=False)
    city_id: Mapped[int | None] = mapped_column(ForeignKey("cities.id"), nullable=True)

    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    province = relationship("Province")
    city = relationship("City")
    work_items: Mapped[list["WorkItem"]] = relationship(  # noqa: F821
        back_populates="site"
    )
