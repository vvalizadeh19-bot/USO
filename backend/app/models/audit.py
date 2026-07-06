"""Audit Domain (§3.18, §7.15) and CPM sync bookkeeping (§2.4).

Audit events are append-only and immutable — no update/delete paths exist.
"""
from __future__ import annotations

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, PKMixin, TimestampMixin
from app.models.enums import ChangeRequestStatus


class AuditLog(Base, PKMixin, TimestampMixin):
    """Immutable audit trail. Stores who/what/when/old/new (§2.23)."""

    __tablename__ = "audit_logs"

    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    module: Mapped[str] = mapped_column(String(60), nullable=False)
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(60), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    old_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)


class CpmImportBatch(Base, PKMixin, TimestampMixin):
    """One CPM import run (§2.4). Summarises what changed."""

    __tablename__ = "cpm_import_batches"

    filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    imported_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    rows_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sites_created: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    work_items_created: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    villages_created: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unchanged: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    change_requests: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    errors: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class ChangeRequest(Base, PKMixin, TimestampMixin):
    """A detected change to an existing record, pending PM decision (§2.4)."""

    __tablename__ = "change_requests"

    batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("cpm_import_batches.id"), nullable=True
    )
    entity_type: Mapped[str] = mapped_column(String(60), nullable=False)
    entity_key: Mapped[str] = mapped_column(String(120), nullable=False)
    field: Mapped[str] = mapped_column(String(80), nullable=False)
    old_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ChangeRequestStatus] = mapped_column(
        Enum(ChangeRequestStatus), default=ChangeRequestStatus.PENDING, nullable=False
    )
    decided_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
