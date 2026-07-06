"""Import all models so ``Base.metadata`` is fully populated."""
from app.models.base import Base
from app.models.master import (
    City,
    Contractor,
    ProblemCategory,
    Province,
)
from app.models.site import Site
from app.models.work_item import WorkItem
from app.models.village import Village, VillageTechApproval
from app.models.user import Role, User
from app.models.audit import AuditLog, ChangeRequest, CpmImportBatch

__all__ = [
    "Base",
    "Province",
    "City",
    "Contractor",
    "ProblemCategory",
    "Site",
    "WorkItem",
    "Village",
    "VillageTechApproval",
    "Role",
    "User",
    "AuditLog",
    "ChangeRequest",
    "CpmImportBatch",
]
