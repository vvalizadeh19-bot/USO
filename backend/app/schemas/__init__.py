"""Pydantic v2 schemas (request/response models)."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- Auth ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserOut(ORMModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    roles: list[str] = []
    region: str | None = None
    contractor_id: int | None = None


# --- Master / Work Item read models ---
class VillageOut(ORMModel):
    id: int
    village_code: str
    name: str | None = None
    village_type: str | None = None


class WorkItemOut(ORMModel):
    id: int
    site_code: str
    site_type: str
    requested_technologies: list[str] = []
    assignment_date: date | None = None
    on_air_date: date | None = None
    last_site_status: str | None = None
    status: str
    province: str | None = None
    city: str | None = None
    is_temporary_site: bool = False
    villages: list[VillageOut] = []


class WorkItemListItem(ORMModel):
    id: int
    site_code: str
    site_type: str
    status: str
    province: str | None = None
    village_count: int = 0


# --- CPM import ---
class ChangeRequestOut(ORMModel):
    id: int
    entity_type: str
    entity_key: str
    field: str
    old_value: str | None = None
    new_value: str | None = None
    status: str


class CpmImportSummary(BaseModel):
    batch_id: int
    filename: str | None = None
    rows_total: int
    sites_created: int
    work_items_created: int
    villages_created: int
    unchanged: int
    change_requests: int
    errors: int
    imported_at: datetime


# --- Dashboard ---
class DashboardKPIs(BaseModel):
    total_sites: int
    total_work_items: int
    total_villages: int
    on_air_sites: int
    temporary_sites: int
    work_items_by_status: dict[str, int]
    work_items_by_site_type: dict[str, int]
    villages_by_province: dict[str, int]
    fully_accepted: int
    pending_change_requests: int
