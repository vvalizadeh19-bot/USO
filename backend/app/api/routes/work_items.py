"""Work Item read endpoints with row-level visibility (§7.8).

Regional Managers see only their region's provinces. (Contractor scoping will
attach once the Assignment module lands; the hook is already here.)
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.site import Site
from app.models.user import RoleName, User
from app.models.work_item import WorkItem
from app.schemas import WorkItemListItem, WorkItemOut

router = APIRouter(prefix="/work-items", tags=["work-items"])


def _scoped_query(db: Session, user: User):
    q = (
        db.query(WorkItem)
        .join(Site, WorkItem.site_id == Site.id)
        .options(joinedload(WorkItem.site).joinedload(Site.province),
                 joinedload(WorkItem.villages))
        .filter(WorkItem.is_deleted.is_(False))
    )
    # Row-level security: regional managers restricted to their region.
    if RoleName.REGIONAL_MANAGER.value in user.role_names and not (
        {RoleName.ADMIN.value, RoleName.PROJECT_MANAGER.value} & user.role_names
    ):
        if user.region:
            q = q.filter(Site.province.has(region=user.region))
        else:
            q = q.filter(False)  # no region assigned -> see nothing
    return q


def _to_out(wi: WorkItem) -> WorkItemOut:
    return WorkItemOut(
        id=wi.id,
        site_code=wi.site.site_code,
        site_type=wi.site_type.value,
        requested_technologies=wi.requested_technologies,
        assignment_date=wi.assignment_date,
        on_air_date=wi.on_air_date,
        last_site_status=wi.last_site_status,
        status=wi.status.value,
        province=wi.site.province.name if wi.site.province else None,
        city=wi.site.city.name if wi.site.city else None,
        is_temporary_site=wi.site.is_temporary,
        villages=[
            {"id": v.id, "village_code": v.village_code, "name": v.name,
             "village_type": v.village_type.value if v.village_type else None}
            for v in wi.villages
        ],
    )


@router.get("", response_model=list[WorkItemListItem])
def list_work_items(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    province: str | None = Query(None),
    site_type: str | None = Query(None),
    q: str | None = Query(None, description="Search by site code"),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
) -> list[WorkItemListItem]:
    query = _scoped_query(db, user)
    if province:
        query = query.filter(Site.province.has(name=province))
    if site_type:
        query = query.filter(WorkItem.site_type == site_type)
    if q:
        query = query.filter(Site.site_code.ilike(f"%{q}%"))
    items = query.order_by(WorkItem.id).offset(offset).limit(limit).all()
    return [
        WorkItemListItem(
            id=wi.id,
            site_code=wi.site.site_code,
            site_type=wi.site_type.value,
            status=wi.status.value,
            province=wi.site.province.name if wi.site.province else None,
            village_count=len(wi.villages),
        )
        for wi in items
    ]


@router.get("/{work_item_id}", response_model=WorkItemOut)
def get_work_item(
    work_item_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> WorkItemOut:
    wi = _scoped_query(db, user).filter(WorkItem.id == work_item_id).one_or_none()
    if wi is None:
        raise HTTPException(status_code=404, detail="Work item not found")
    return _to_out(wi)
