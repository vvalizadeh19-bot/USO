"""Declarative base and shared mixins.

Invariants enforced here (Domain §3.22):
  - Soft Delete only — operational records are never physically deleted (§2.24).
  - Every row carries created/updated timestamps for auditability (§2.23).
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=utcnow,
        nullable=False,
    )


class SoftDeleteMixin:
    """Soft delete support (§2.24). Deleted rows stay recoverable."""

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.deleted_at = utcnow()


class PKMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
