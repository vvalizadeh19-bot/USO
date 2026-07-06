"""Work Item — the core Aggregate Root (§3.4).

Business key: Site + Site Type (§2.5). Requested technology is parsed from the
packed CPM string (e.g. ``2G3G4G``) into independent boolean flags. DT/lifecycle
status is derived by the workflow engine; it is stored here as the current state.
"""
from __future__ import annotations

from sqlalchemy import Boolean, Date, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, PKMixin, SoftDeleteMixin, TimestampMixin
from app.models.enums import SiteType, WorkItemStatus


class WorkItem(Base, PKMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "work_items"
    __table_args__ = (
        UniqueConstraint("site_id", "site_type", name="uq_workitem_site_type"),
    )

    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False)
    site_type: Mapped[SiteType] = mapped_column(Enum(SiteType), nullable=False)

    # Requested technology (§2.16) — parsed from CPM "2G3G4G" style string.
    requested_technology_raw: Mapped[str | None] = mapped_column(String(20), nullable=True)
    requires_2g: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requires_3g: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requires_4g: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Dates owned by CPM (§2.3).
    assignment_date: Mapped["Date | None"] = mapped_column(Date, nullable=True)  # official assignment
    on_air_date: Mapped["Date | None"] = mapped_column(Date, nullable=True)

    last_site_status: Mapped[str | None] = mapped_column(String(60), nullable=True)  # آخرین مرحله

    status: Mapped[WorkItemStatus] = mapped_column(
        Enum(WorkItemStatus), default=WorkItemStatus.NEW, nullable=False
    )

    site = relationship("Site", back_populates="work_items")
    villages: Mapped[list["Village"]] = relationship(  # noqa: F821
        back_populates="work_item", cascade="all, delete-orphan"
    )

    @property
    def requested_technologies(self) -> list[str]:
        out = []
        if self.requires_2g:
            out.append("2G")
        if self.requires_3g:
            out.append("3G")
        if self.requires_4g:
            out.append("4G")
        return out
