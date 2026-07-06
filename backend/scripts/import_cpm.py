"""CLI: import a CPM .xlsx file.

Usage:
    python -m scripts.import_cpm data/CPM_sample.xlsx [--header-row N]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running as a script from the backend/ directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal  # noqa: E402
from app.core.init_db import init  # noqa: E402
from app.services.cpm_import import CpmImportService  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a CPM Excel file.")
    parser.add_argument("path", help="Path to the CPM .xlsx file")
    parser.add_argument("--header-row", type=int, default=None)
    args = parser.parse_args()

    init()  # ensure tables + seed exist
    db = SessionLocal()
    try:
        service = CpmImportService(db)
        batch, result = service.import_file(
            args.path, filename=Path(args.path).name, header_row=args.header_row
        )
        print(json.dumps(result.as_summary(), indent=2))
        if result.change_requests:
            print("\nChange Requests:")
            print(json.dumps(result.change_requests, indent=2, ensure_ascii=False))
        if result.errors:
            print("\nErrors:")
            print(json.dumps(result.errors, indent=2, ensure_ascii=False))
    finally:
        db.close()


if __name__ == "__main__":
    main()
