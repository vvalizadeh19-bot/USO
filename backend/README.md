# USO Enterprise Platform — Backend

FastAPI backend for the USO Enterprise Platform (UEP). Built entirely on
**free / open-source** technologies, per the requirements specification
([Chapter 7](../docs/requirements/07-security-architecture.md)).

## Tech stack (all non-paid)

| Concern | Technology | License |
|---------|-----------|---------|
| Web framework | FastAPI + Uvicorn | MIT / BSD |
| ORM | SQLAlchemy 2.0 | MIT |
| Database | PostgreSQL (prod) / SQLite (dev) | PostgreSQL / Public Domain |
| Validation | Pydantic v2 | MIT |
| Auth | JWT (python-jose) | MIT |
| Password hashing | Argon2id (passlib) | BSD |
| Excel parsing | openpyxl | MIT |
| Tests | pytest + httpx | MIT / BSD |

## What is implemented in this first cut

This slice delivers the **CPM ingestion pipeline and core domain**, which the
whole platform is built around:

- **Domain model** (Chapter 3): Master Data, Site, Work Item (aggregate root),
  Village, per-technology Acceptance, Users/Roles, Audit, CPM batches/change
  requests. Soft delete + timestamps on all operational entities.
- **CPM Import Service** (§2.3–2.4): parses the real monthly `.xlsx`,
  maps columns by **name** (Persian *or* English), handles the `No Site ID`
  temporary-code fallback, parses packed technology strings (`2G3G4G`), groups
  rows into Site → Work Item → Village, and applies the sync rules
  (new → create, unchanged → ignore, changed → **Change Request** for PM
  decision — never silent overwrite).
- **Auth & RBAC** (Chapter 7): password login, JWT access/refresh tokens,
  Argon2id hashing, role-based route guards, and a row-level visibility hook
  (regional managers scoped to their region).
- **Dashboard KPIs** (§2.26, §3.13): computed on read, never stored.
- **REST API**: `/auth`, `/work-items`, `/dashboard`, `/cpm`.

> Not yet built (reserved for later slices): Health Check, Assignment, Drive
> Test and Acceptance *write* workflows, Notification & Action Center engines,
> Reporting exports. The models and enums for these already exist so the
> workflow services can be layered on without schema changes.

## Quick start

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # optional; defaults work out of the box

# Run the API (creates tables + seeds admin/roles on startup)
uvicorn app.main:app --reload
```

Then open the interactive docs at <http://localhost:8000/docs>.

Default bootstrap admin: **`admin` / `ChangeMe!Admin1`** (change via `.env`).

### Import a CPM file

From the CLI:

```bash
python -m scripts.import_cpm data/CPM_sample.xlsx
# add --header-row N to force a specific header row
```

Or via the API (Admin / PM only):

```bash
TOKEN=$(curl -s -X POST localhost:8000/api/auth/login \
  -d 'username=admin&password=ChangeMe!Admin1' | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

curl -X POST localhost:8000/api/cpm/import \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@data/CPM_sample.xlsx"
```

## CPM file expectations

The importer keys off **header names**, so column order in the 69-column monthly
file can change safely. It accepts the original Persian headers *or* these
standardized English names (recommended for future-proofing):

```
village_id | province | city | site_id | temp_site_id |
site_assignment_date | site_type | requested_technology |
on_air_date | last_site_status | village_type
```

Notes on the real data:

- The header row is **auto-detected** (the row containing a `site_id` column).
  In the sample it is row 3; rows 1–2 are summary stats.
- `site_id` is often `"No Site ID"` — the importer falls back to `temp_site_id`
  (`کدسایت موقت`) as the effective site code and flags the site as temporary. A
  later real Site ID raises a Change Request rather than overwriting.
- `requested_technology` is a packed string (`2G3G4G`, `3G4G`, …) → parsed into
  `requires_2g/3g/4g` flags.

A copy of the sample file lives at [`data/CPM_sample.xlsx`](data/CPM_sample.xlsx)
and is used by the tests.

## Tests

```bash
cd backend
python -m pytest -q
```

Covers value parsers, import counts, the temporary-site fallback, multi-village
grouping, tech-approval materialization, idempotent re-import, change-request
detection, and the API auth/RBAC/dashboard flows.

## Project layout

```
backend/
├── app/
│   ├── core/        config, database, security (JWT/Argon2), deps (RBAC), init/seed
│   ├── models/      SQLAlchemy models + enums (the domain model)
│   ├── schemas/     Pydantic request/response models
│   ├── services/    cpm_import.py (CPM ingestion pipeline)
│   ├── api/routes/  auth, work_items, dashboard, cpm
│   └── main.py      FastAPI app
├── scripts/         import_cpm.py (CLI)
├── data/            CPM_sample.xlsx
├── tests/           pytest suite
└── requirements.txt
```
