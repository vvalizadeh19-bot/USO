"""Tests for the CPM import service against the real sample file."""
from __future__ import annotations

import openpyxl

from app.models.site import Site
from app.models.village import Village, VillageTechApproval
from app.models.work_item import WorkItem
from app.services.cpm_import import (
    CpmImportService,
    parse_date,
    parse_site_type,
    parse_technologies,
    parse_village_type,
)
from tests.conftest import SAMPLE_CPM


def test_value_parsers():
    assert parse_technologies("2G3G4G") == {
        "requires_2g": True, "requires_3g": True, "requires_4g": True}
    assert parse_technologies("3G4G")["requires_2g"] is False
    assert parse_site_type("New Site").value == "New Site"
    assert parse_site_type("Add Tech").value == "Add Tech"
    assert parse_village_type("هدف").value == "Target"
    assert parse_village_type("اقماری").value == "Satellite"
    assert parse_date("2022-01-05").isoformat() == "2022-01-05"
    assert parse_date("No Site ID") is None


def test_import_sample_counts(db_session):
    service = CpmImportService(db_session)
    batch, result = service.import_file(SAMPLE_CPM, filename="CPM_sample.xlsx")

    assert result.rows_total == 43
    assert result.errors == []
    # 43 rows collapse into fewer sites/work-items (one site → many villages).
    assert result.villages_created == 43
    assert result.work_items_created == db_session.query(WorkItem).count()
    assert result.sites_created == db_session.query(Site).count()
    # Every row yields exactly one village.
    assert db_session.query(Village).count() == 43


def test_temp_site_fallback(db_session):
    """Rows with 'No Site ID' must key off the temporary code."""
    CpmImportService(db_session).import_file(SAMPLE_CPM)
    temp_sites = db_session.query(Site).filter(Site.is_temporary.is_(True)).all()
    assert temp_sites, "expected at least one temporary site in the sample"
    for s in temp_sites:
        assert s.irancell_site_id is None
        assert s.temp_site_id and s.site_code == s.temp_site_id


def test_multi_village_grouping(db_session):
    CpmImportService(db_session).import_file(SAMPLE_CPM)
    multi = [wi for wi in db_session.query(WorkItem).all() if len(wi.villages) > 1]
    assert multi, "sample contains sites with multiple villages"


def test_tech_approvals_materialized(db_session):
    CpmImportService(db_session).import_file(SAMPLE_CPM)
    # Approvals exist for both phases.
    phases = {r.phase for r in db_session.query(VillageTechApproval).all()}
    assert phases == {"ICT", "CRA"}


def test_idempotent_reimport(db_session):
    service = CpmImportService(db_session)
    service.import_file(SAMPLE_CPM)
    sites, wis, villages = (
        db_session.query(Site).count(),
        db_session.query(WorkItem).count(),
        db_session.query(Village).count(),
    )
    _, result2 = service.import_file(SAMPLE_CPM)
    assert result2.sites_created == 0
    assert result2.work_items_created == 0
    assert result2.villages_created == 0
    assert result2.change_requests == []
    assert db_session.query(Site).count() == sites
    assert db_session.query(WorkItem).count() == wis
    assert db_session.query(Village).count() == villages


def test_change_request_on_modified_value(db_session, tmp_path):
    """Altering a tracked field on re-import must raise a Change Request, not overwrite."""
    service = CpmImportService(db_session)
    service.import_file(SAMPLE_CPM)

    # Build a modified copy: change the last-site-status of the first data row.
    wb = openpyxl.load_workbook(SAMPLE_CPM)
    ws = wb.active
    ws.cell(row=4, column=24).value = "CHANGED_STATUS"
    modified = tmp_path / "CPM_modified.xlsx"
    wb.save(modified)

    _, result = service.import_file(str(modified))
    assert len(result.change_requests) >= 1
    assert any(cr["new"] == "CHANGED_STATUS" for cr in result.change_requests)
    # Original value must be preserved (not silently overwritten).
    wi = db_session.query(WorkItem).all()
    assert all(w.last_site_status != "CHANGED_STATUS" for w in wi)
