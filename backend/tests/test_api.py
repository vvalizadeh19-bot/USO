"""API smoke tests: auth flow, RBAC, dashboard, work-item listing."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.core.init_db import seed
from app.main import app
from app.models import Base
from app.services.cpm_import import CpmImportService
from tests.conftest import SAMPLE_CPM


@pytest.fixture()
def client(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path/'api.db'}", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    db = Session()
    seed(db)
    CpmImportService(db).import_file(SAMPLE_CPM)
    db.close()

    def override_get_db():
        d = Session()
        try:
            yield d
        finally:
            d.close()

    # Use TestClient without a 'with' block so the startup lifespan (which would
    # build its own DB) never runs; the DB above is already seeded and imported.
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def _login(client, username="admin", password="ChangeMe!Admin1"):
    resp = client.post(
        "/api/auth/login", data={"username": username, "password": password}
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_login_and_me(client):
    token = _login(client)
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert "Administrator" in me.json()["roles"]


def test_login_bad_password(client):
    resp = client.post("/api/auth/login", data={"username": "admin", "password": "wrong"})
    assert resp.status_code == 401


def test_requires_auth(client):
    assert client.get("/api/work-items").status_code == 401


def test_dashboard_kpis(client):
    token = _login(client)
    resp = client.get("/api/dashboard/kpis", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_villages"] == 43
    assert data["total_work_items"] == 33
    assert data["temporary_sites"] > 0


def test_work_item_listing_and_detail(client):
    token = _login(client)
    h = {"Authorization": f"Bearer {token}"}
    lst = client.get("/api/work-items?limit=5", headers=h)
    assert lst.status_code == 200 and len(lst.json()) == 5
    wid = lst.json()[0]["id"]
    detail = client.get(f"/api/work-items/{wid}", headers=h)
    assert detail.status_code == 200
    assert "villages" in detail.json()
