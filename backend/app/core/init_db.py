"""Create tables and seed baseline data (roles, admin user, problem categories)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal, engine
from app.core.security import hash_password
from app.models import Base
from app.models.master import DEFAULT_PROBLEM_CATEGORIES, ProblemCategory
from app.models.user import Role, RoleName, User


def create_all() -> None:
    Base.metadata.create_all(bind=engine)


def seed(db: Session) -> None:
    # Roles (§7.6)
    roles: dict[str, Role] = {}
    for rn in RoleName:
        role = db.query(Role).filter(Role.name == rn.value).one_or_none()
        if role is None:
            role = Role(name=rn.value)
            db.add(role)
            db.flush()
        roles[rn.value] = role

    # Default problem categories (§2.8)
    for name in DEFAULT_PROBLEM_CATEGORIES:
        if not db.query(ProblemCategory).filter(ProblemCategory.name == name).count():
            db.add(ProblemCategory(name=name))

    # Bootstrap admin
    admin = db.query(User).filter(User.username == settings.admin_username).one_or_none()
    if admin is None:
        admin = User(
            username=settings.admin_username,
            email=settings.admin_email,
            full_name="System Administrator",
            hashed_password=hash_password(settings.admin_password),
        )
        admin.roles.append(roles[RoleName.ADMIN.value])
        db.add(admin)

    db.commit()


def init() -> None:
    create_all()
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    init()
    print("Database initialised and seeded.")
