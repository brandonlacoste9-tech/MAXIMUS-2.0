"""
tests/test_lead_logger.py — MAXIMUS Sovereign Command
Unit tests for the lead_logger module.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from lead_logger import _CSV_HEADERS, _ensure_csv, log_lead


class TestEnsureCsv:
    def test_creates_file_with_headers(self, tmp_path):
        csv_file = tmp_path / "sub" / "leads.csv"
        _ensure_csv(csv_file)
        assert csv_file.exists()
        with csv_file.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            assert reader.fieldnames == _CSV_HEADERS

    def test_does_not_overwrite_existing(self, tmp_path):
        csv_file = tmp_path / "leads.csv"
        csv_file.write_text("existing content")
        _ensure_csv(csv_file)
        assert csv_file.read_text() == "existing content"


class TestLogLead:
    def test_appends_row(self, tmp_path):
        csv_file = tmp_path / "leads.csv"
        log_lead(
            csv_path=csv_file,
            user_id=123,
            username="testuser",
            action="DISPATCH_REQUEST",
            service_type="PLOMBERIE",
            raw_text="Mon lavabo fuit",
        )
        with csv_file.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert len(rows) == 1
        assert rows[0]["user_id"] == "123"
        assert rows[0]["action"] == "DISPATCH_REQUEST"
        assert rows[0]["service_type"] == "PLOMBERIE"
        assert rows[0]["raw_text"] == "Mon lavabo fuit"

    def test_multiple_rows(self, tmp_path):
        csv_file = tmp_path / "leads.csv"
        for i in range(3):
            log_lead(csv_file, user_id=i, username=f"user{i}", action="TEST")
        with csv_file.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert len(rows) == 3
