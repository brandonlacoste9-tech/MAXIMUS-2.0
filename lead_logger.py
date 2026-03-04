"""
lead_logger.py — MAXIMUS SOVEREIGN COMMAND
Tier-1 Reflex Layer: persists every user interaction to CSV and Excel
for the central Lead Command dashboard.

File layout
-----------
data/
  leads_YYYY-MM-DD.csv    — daily append-only log
  leads_master.xlsx       — rolling master workbook (all time)
"""

import os
import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from config import LEADS_DIR

logger = logging.getLogger(__name__)

# Column schema — keep consistent across all writes
_COLUMNS = [
    "timestamp",
    "user_id",
    "username",
    "full_name",
    "action",       # e.g. /start, DISPATCH, RECRUITMENT
    "raw_message",
    "service_type", # populated for DISPATCH actions
    "pillar",       # MAX | Q-MÉTIER | Q-EMPLOIS | FLOGURU
]

_MASTER_FILE = "leads_master.xlsx"


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _daily_csv_path(base: Path) -> Path:
    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    return base / f"leads_{today}.csv"


def log_interaction(
    user_id: int,
    username: str,
    full_name: str,
    action: str,
    raw_message: str = "",
    service_type: str = "",
    pillar: str = "MAX",
) -> None:
    """
    Append one interaction row to the daily CSV and the master Excel workbook.

    Parameters
    ----------
    user_id:      Telegram numeric user ID.
    username:     Telegram @handle (may be empty string).
    full_name:    Display name of the user.
    action:       High-level action label (e.g. DISPATCH, RECRUITMENT, /start).
    raw_message:  Original text the user sent.
    service_type: Classified service (populated for DISPATCH flows).
    pillar:       Active MAXIMUS pillar routing this request.
    """
    base = Path(LEADS_DIR)
    _ensure_dir(base)

    row = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "user_id": user_id,
        "username": username or "",
        "full_name": full_name or "",
        "action": action,
        "raw_message": raw_message,
        "service_type": service_type,
        "pillar": pillar,
    }

    # ── Daily CSV (append) ────────────────────────────────────
    csv_path = _daily_csv_path(base)
    new_df = pd.DataFrame([row], columns=_COLUMNS)
    write_header = not csv_path.exists()
    new_df.to_csv(csv_path, mode="a", header=write_header, index=False)
    logger.debug("Lead logged to CSV: %s", csv_path)

    # ── Master Excel workbook (read → append → write) ─────────
    xlsx_path = base / _MASTER_FILE
    if xlsx_path.exists():
        try:
            existing = pd.read_excel(xlsx_path, engine="openpyxl")
            combined = pd.concat([existing, new_df], ignore_index=True)
        except Exception as exc:  # pragma: no cover
            logger.error("Could not read master workbook, recreating: %s", exc)
            combined = new_df
    else:
        combined = new_df

    combined.to_excel(xlsx_path, index=False, engine="openpyxl")
    logger.debug("Lead logged to Excel: %s", xlsx_path)
