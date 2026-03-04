"""
lead_logger.py — MAXIMUS Sovereign Command
Tier-3 Worker: persists every client interaction to a local CSV file
(and optionally an Excel workbook) for the central command dashboard.

All data stays on-premise — Bill 96 / Law 25 compliant by design.
"""

from __future__ import annotations

import csv
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_CSV_HEADERS = [
    "timestamp",
    "user_id",
    "username",
    "action",
    "service_type",
    "raw_text",
]


def _ensure_csv(path: Path) -> None:
    """Create the CSV file with headers if it does not yet exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_CSV_HEADERS)
            writer.writeheader()


def log_lead(
    csv_path: str | os.PathLike[str],
    user_id: int | str,
    username: str,
    action: str,
    service_type: str = "",
    raw_text: str = "",
) -> None:
    """
    Append one row to the leads CSV.

    Parameters
    ----------
    csv_path:     Destination file path (created on first call).
    user_id:      Telegram user ID.
    username:     Telegram ``@handle`` or full name.
    action:       High-level action label, e.g. ``"DISPATCH_REQUEST"``.
    service_type: Classified service type returned by dispatch_bridge.
    raw_text:     Original free-text message from the user.
    """
    path = Path(csv_path)
    _ensure_csv(path)

    row: dict[str, Any] = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "user_id": user_id,
        "username": username,
        "action": action,
        "service_type": service_type,
        "raw_text": raw_text,
    }

    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=_CSV_HEADERS)
        writer.writerow(row)

    logger.info("Lead logged → %s | %s | %s", user_id, action, service_type)


def export_to_excel(csv_path: str | os.PathLike[str], xlsx_path: str | os.PathLike[str]) -> None:
    """
    Convert the leads CSV to an Excel workbook (.xlsx).

    Requires ``openpyxl`` (already in requirements.txt).
    """
    import openpyxl  # noqa: PLC0415 — optional heavy import

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Leads"

    csv_file = Path(csv_path)
    if not csv_file.exists():
        logger.warning("CSV not found at %s — creating empty workbook.", csv_path)
        wb.save(xlsx_path)
        return

    with csv_file.open(newline="", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            ws.append(row)

    wb.save(xlsx_path)
    logger.info("Leads exported to Excel → %s", xlsx_path)
