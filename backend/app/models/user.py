"""Users, Roles and RBAC (§7.6). Role/permission data is stored in the database
so Admin can change access without redeployment (Security Recommendation 1).
"""
from __future__ import annotations

import enum

from sqlalchemy import Boolean, ForeignKey, String, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, PKMixin, SoftDeleteMixin, TimestampMixin


class RoleName(str, enum.Enum):
    ADMIN = "Administrator"
    PROJECT_MANAGER = "Project Manager"
    COORDINATOR = "Coordinator"
    REGIONAL_MANAGER = "Regional Manager"
    CONTRACTOR = "Contractor"
    VIEWER = "Viewer"


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class Role(Base, PKMixin, TimestampMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    users: Mapped[list["User"]] = relationship(
        secondary=user_roles, back_populates="roles"
    )


class User(Base, PKMixin, TimestampMixin, SoftDeleteMixin):
    """Aggregate Root (§3.19)."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Row-level scoping (§7.8): contractor users see only their own data;
    # regional managers see only their region.
    contractor_id: Mapped[int | None] = mapped_column(
        ForeignKey("contractors.id"), nullable=True
    )
    region: Mapped[str | None] = mapped_column(String(60), nullable=True)

    roles: Mapped[list[Role]] = relationship(
        secondary=user_roles, back_populates="users"
    )

    @property
    def role_names(self) -> set[str]:
        return {r.name for r in self.roles}
