"""Dashboard Domain (§3.13, §2.26). Values are always calculated, never stored."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.audit import ChangeRequest
from app.models.enums import ChangeRequestStatus
from app.models.master import Province
from app.models.site import Site
from app.models.user import User
from app.models.village import Village
from app.models.work_item import WorkItem
from app.schemas import DashboardKPIs

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/kpis", response_model=DashboardKPIs)
def kpis(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> DashboardKPIs:
    active_site = Site.is_deleted.is_(False)
    active_wi = WorkItem.is_deleted.is_(False)

    by_status = dict(
        db.query(WorkItem.status, func.count(WorkItem.id))
        .filter(active_wi)
        .group_by(WorkItem.status)
        .all()
    )
    by_type = dict(
        db.query(WorkItem.site_type, func.count(WorkItem.id))
        .filter(active_wi)
        .group_by(WorkItem.site_type)
        .all()
    )
    by_province = dict(
        db.query(Province.name, func.count(Village.id))
        .join(Site, Site.province_id == Province.id)
        .join(WorkItem, WorkItem.site_id == Site.id)
        .join(Village, Village.work_item_id == WorkItem.id)
        .filter(Village.is_deleted.is_(False))
        .group_by(Province.name)
        .all()
    )

    return DashboardKPIs(
        total_sites=db.query(func.count(Site.id)).filter(active_site).scalar() or 0,
        total_work_items=db.query(func.count(WorkItem.id)).filter(active_wi).scalar() or 0,
        total_villages=db.query(func.count(Village.id))
        .filter(Village.is_deleted.is_(False)).scalar() or 0,
        on_air_sites=db.query(func.count(WorkItem.id))
        .filter(active_wi, WorkItem.on_air_date.isnot(None)).scalar() or 0,
        temporary_sites=db.query(func.count(Site.id))
        .filter(active_site, Site.is_temporary.is_(True)).scalar() or 0,
        work_items_by_status={k.value: v for k, v in by_status.items()},
        work_items_by_site_type={k.value: v for k, v in by_type.items()},
        villages_by_province=by_province,
        fully_accepted=0,  # derived once Acceptance module is populated (§2.18)
        pending_change_requests=db.query(func.count(ChangeRequest.id))
        .filter(ChangeRequest.status == ChangeRequestStatus.PENDING).scalar() or 0,
    )
