"""CPM import & change-request routes (§2.4). Restricted to Admin / PM (§7.7)."""
from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles
from app.models.audit import ChangeRequest, CpmImportBatch
from app.models.enums import ChangeRequestStatus
from app.models.user import RoleName, User
from app.schemas import ChangeRequestOut, CpmImportSummary
from app.services.cpm_import import CpmImportService

router = APIRouter(prefix="/cpm", tags=["cpm"])

MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # §7.14
ALLOWED_SUFFIXES = {".xlsx", ".xlsm"}

_pm_admin = require_roles(RoleName.ADMIN.value, RoleName.PROJECT_MANAGER.value)


@router.post("/import", response_model=CpmImportSummary)
async def import_cpm(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(_pm_admin),
) -> CpmImportSummary:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(400, f"Unsupported file type '{suffix}'. Expected .xlsx")
    contents = await file.read()
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "File exceeds 20 MB limit")

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
        tmp.write(contents)
        tmp.flush()
        batch, result = CpmImportService(db).import_file(
            tmp.name, filename=file.filename, imported_by=user.id
        )

    return CpmImportSummary(
        batch_id=batch.id,
        filename=batch.filename,
        rows_total=batch.rows_total,
        sites_created=batch.sites_created,
        work_items_created=batch.work_items_created,
        villages_created=batch.villages_created,
        unchanged=batch.unchanged,
        change_requests=batch.change_requests,
        errors=batch.errors,
        imported_at=batch.created_at,
    )


@router.get("/imports", response_model=list[CpmImportSummary])
def list_imports(db: Session = Depends(get_db), user: User = Depends(_pm_admin)):
    batches = db.query(CpmImportBatch).order_by(CpmImportBatch.id.desc()).limit(50).all()
    return [
        CpmImportSummary(
            batch_id=b.id, filename=b.filename, rows_total=b.rows_total,
            sites_created=b.sites_created, work_items_created=b.work_items_created,
            villages_created=b.villages_created, unchanged=b.unchanged,
            change_requests=b.change_requests, errors=b.errors, imported_at=b.created_at,
        )
        for b in batches
    ]


@router.get("/change-requests", response_model=list[ChangeRequestOut])
def list_change_requests(
    status_filter: ChangeRequestStatus | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(_pm_admin),
):
    q = db.query(ChangeRequest)
    if status_filter:
        q = q.filter(ChangeRequest.status == status_filter)
    return q.order_by(ChangeRequest.id.desc()).limit(200).all()
