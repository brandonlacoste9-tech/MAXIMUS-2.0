"""
tests/test_dispatch_bridge.py — MAXIMUS Sovereign Command
Unit tests for the dispatch_bridge module.

These tests use the keyword-fallback path (no Ollama running required)
and also verify the LLM integration path via mocking.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from dispatch_bridge import SERVICE_TYPES, _keyword_fallback, classify_request


# ---------------------------------------------------------------------------
# _keyword_fallback
# ---------------------------------------------------------------------------


class TestKeywordFallback:
    def test_plomberie_fuit(self):
        assert _keyword_fallback("Mon lavabo fuit") == "PLOMBERIE"

    def test_plomberie_tuyau(self):
        assert _keyword_fallback("Le tuyau est bouché") == "PLOMBERIE"

    def test_electricite_french(self):
        assert _keyword_fallback("J'ai besoin d'un électricien") == "ÉLECTRICITÉ"

    def test_electricite_english(self):
        assert _keyword_fallback("My electrical panel is broken") == "ÉLECTRICITÉ"

    def test_menage(self):
        assert _keyword_fallback("Besoin d'un ménage complet") == "MÉNAGE"

    def test_demenagement(self):
        assert _keyword_fallback("Je dois déménager samedi") == "DÉMÉNAGEMENT"

    def test_jardinage(self):
        assert _keyword_fallback("Tondre le gazon") == "JARDINAGE"

    def test_reparation(self):
        assert _keyword_fallback("Réparer ma fenêtre") == "RÉPARATION"

    def test_peinture(self):
        assert _keyword_fallback("Peindre le salon") == "PEINTURE"

    def test_autre_unknown(self):
        assert _keyword_fallback("Je ne sais pas quoi faire") == "AUTRE"

    def test_empty_string(self):
        assert _keyword_fallback("") == "AUTRE"


# ---------------------------------------------------------------------------
# classify_request — fallback when Ollama is unavailable
# ---------------------------------------------------------------------------


class TestClassifyRequestFallback:
    def test_falls_back_on_connection_error(self):
        import requests as req

        with patch("dispatch_bridge.requests.post", side_effect=req.exceptions.ConnectionError("refused")):
            result = classify_request("Mon lavabo fuit")
        assert result == "PLOMBERIE"

    def test_empty_text_returns_autre(self):
        result = classify_request("")
        assert result == "AUTRE"

    def test_whitespace_text_returns_autre(self):
        result = classify_request("   ")
        assert result == "AUTRE"


# ---------------------------------------------------------------------------
# classify_request — LLM happy path
# ---------------------------------------------------------------------------


class TestClassifyRequestLLM:
    def _mock_response(self, text: str) -> MagicMock:
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"response": text}
        return resp

    def test_llm_valid_service_type(self):
        with patch("dispatch_bridge.requests.post", return_value=self._mock_response("PLOMBERIE")):
            assert classify_request("Mon lavabo fuit") == "PLOMBERIE"

    def test_llm_returns_lowercase_falls_back(self):
        # LLM returns lowercase → not in SERVICE_TYPES → keyword fallback
        with patch("dispatch_bridge.requests.post", return_value=self._mock_response("plomberie")):
            assert classify_request("Mon lavabo fuit") == "PLOMBERIE"

    def test_llm_unexpected_token_falls_back(self):
        with patch(
            "dispatch_bridge.requests.post",
            return_value=self._mock_response("I don't know"),
        ):
            assert classify_request("Le tuyau est cassé") == "PLOMBERIE"

    def test_llm_electricite(self):
        with patch(
            "dispatch_bridge.requests.post",
            return_value=self._mock_response("ÉLECTRICITÉ"),
        ):
            assert classify_request("Besoin d'un électricien") == "ÉLECTRICITÉ"


# ---------------------------------------------------------------------------
# SERVICE_TYPES completeness
# ---------------------------------------------------------------------------


def test_service_types_non_empty():
    assert len(SERVICE_TYPES) > 0


def test_autre_always_in_service_types():
    assert "AUTRE" in SERVICE_TYPES
