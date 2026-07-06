"""Village (§3.5) and per-technology acceptance (§3.11).

A Village belongs to exactly one Work Item (invariant §3.22.2). Acceptance is
tracked per Village + per technology, independently for ICT and CRA (§2.14–2.17).
"""
from __future__ import annotations

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, PKMixin, SoftDeleteMixin, TimestampMixin
from app.models.enums import ApprovalStatus, Technology, VillageType


class Village(Base, PKMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "villages"
    __table_args__ = (
        UniqueConstraint("work_item_id", "village_code", name="uq_village_workitem"),
    )

    work_item_id: Mapped[int] = mapped_column(ForeignKey("work_items.id"), nullable=False)
    village_code: Mapped[str] = mapped_column(String(40), nullable=False, index=True)  # کد آبادی
    name: Mapped[str | None] = mapped_column(String(160), nullable=True)  # آبادی
    village_type: Mapped[VillageType | None] = mapped_column(Enum(VillageType), nullable=True)

    work_item = relationship("WorkItem", back_populates="villages")
    tech_approvals: Mapped[list["VillageTechApproval"]] = relationship(
        back_populates="village", cascade="all, delete-orphan"
    )


class VillageTechApproval(Base, PKMixin, TimestampMixin):
    """Independent approval status per (village, phase, technology) (§3.11)."""

    __tablename__ = "village_tech_approvals"
    __table_args__ = (
        UniqueConstraint(
            "village_id", "phase", "technology", name="uq_village_phase_tech"
        ),
    )

    village_id: Mapped[int] = mapped_column(ForeignKey("villages.id"), nullable=False)
    phase: Mapped[str] = mapped_column(String(8), nullable=False)  # "ICT" | "CRA"
    technology: Mapped[Technology] = mapped_column(Enum(Technology), nullable=False)
    status: Mapped[ApprovalStatus] = mapped_column(
        Enum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False
    )

    village = relationship("Village", back_populates="tech_approvals")
