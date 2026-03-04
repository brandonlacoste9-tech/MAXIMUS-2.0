# 🏛️ MAXIMUS SOVEREIGN COMMAND

> **La Souveraineté Numérique au Service du Travail Québécois** 👑🚀✨🏆💎✅

MAXIMUS SOVEREIGN COMMAND is the top-level orchestrator for a **4-pillar AI empire** serving
the autonomous labour marketplace of Québec.

---

## The 4-Pillar Empire

| Pillar | Role |
|--------|------|
| **MAX** | Core AI brain & routing engine |
| **Q-MÉTIER** | Trade & skilled-worker registry |
| **Q-EMPLOIS** | Job-posting & matching marketplace |
| **FLOGURU** | Flow automation & operations intelligence |

---

## 4-Tier Intelligence Stack

```
┌─────────────────────────────────────────────────┐
│  Tier 1 · REFLEX   — Instant menu / keyboards   │
│  Tier 2 · LOGIC    — dispatch_bridge (LLM)      │
│  Tier 3 · WORKER   — lead_logger (CSV / Excel)  │
│  Tier 4 · VISION   — Ollama local inference     │
└─────────────────────────────────────────────────┘
```

All AI inference runs **locally via Ollama** — zero cloud tokens, zero data leaks.
This is the *Goodbye Tokens* philosophy: your business data never leaves Québec soil.

---

## Project Structure

```
MAXIMUS-2.0/
├── bot.py                 # Telegram bot — Tier 1 Reflex layer
├── dispatch_bridge.py     # NLP → service-type mapping — Tier 2 Logic
├── lead_logger.py         # Lead persistence (CSV/Excel) — Tier 3 Worker
├── config.py              # Central configuration (reads from .env)
├── requirements.txt       # Python dependencies
├── .env.example           # Secret template (copy → .env)
└── tests/
    ├── test_dispatch_bridge.py
    └── test_lead_logger.py
```

---

## Quickstart

### 1 — Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.10+ |
| [Ollama](https://ollama.ai) | latest |

Pull the default model (Mistral runs entirely offline):

```bash
ollama pull mistral
```

### 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### 3 — Configure secrets

```bash
cp .env.example .env
# Edit .env — add your Telegram Bot Token (from @BotFather)
```

### 4 — Launch the Sovereign Executive

```bash
python bot.py
```

---

## Telegram Bot — User Flow

```
/start
  ├── 🔧 Demander un Service   →  describe need (free text)
  │                            →  LLM classifies → logs lead → confirms
  └── 💼 Devenir Tasker        →  submit name + specialty + city
                               →  logs application → confirms
```

### Supported Service Types

`PLOMBERIE` · `ÉLECTRICITÉ` · `MÉNAGE` · `DÉMÉNAGEMENT` · `JARDINAGE` · `RÉPARATION` · `PEINTURE` · `AUTRE`

---

## Lead Dashboard

Every interaction is appended to `data/leads.csv` with columns:

| timestamp | user_id | username | action | service_type | raw_text |
|-----------|---------|----------|--------|--------------|----------|

Export to Excel at any time:

```python
from lead_logger import export_to_excel
export_to_excel("data/leads.csv", "data/leads.xlsx")
```

---

## $50M ARR Roadmap

| Phase | Milestone | Target |
|-------|-----------|--------|
| 0 | Sovereign Executive MVP (this release) | Q1 2025 |
| 1 | Q-MÉTIER — 500 verified Taskers | Q2 2025 |
| 2 | Q-EMPLOIS — automated job matching | Q3 2025 |
| 3 | FLOGURU — operations intelligence dashboard | Q4 2025 |
| 4 | Pan-Québec expansion + WhatsApp channel | Q1 2026 |
| 5 | $50M ARR — 10 000 active Taskers | 2027 |

---

## Goodbye Tokens Philosophy 🔑

Traditional SaaS labour platforms extract value via per-transaction tokens or
percentage fees, leaking revenue to US cloud giants.  MAXIMUS runs every
inference locally (Ollama), stores every byte on-premise, and charges a flat
subscription — **zero extraction, 100 % sovereignty**.

---

## Legal & Compliance 🏛️

| Law | How MAXIMUS complies |
|-----|----------------------|
| **Bill 96** (language) | All client-facing text defaults to French; English supported as secondary |
| **Law 25** (privacy) | No personal data sent to third-party APIs; all data stored locally |

---

## License

MIT © MAXIMUS SOVEREIGN COMMAND
