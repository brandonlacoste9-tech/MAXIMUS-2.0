# 🏛️ MAXIMUS SOVEREIGN COMMAND

> *La Souveraineté Numérique au Service du Travail Québécois.* 👑🚀✨🏆💎✅

**MAXIMUS SOVEREIGN COMMAND** is the top-level orchestrator of a 4-pillar AI labour-marketplace empire for Quebec, targeting **$50 M ARR** through autonomous task-matching, sovereign LLM inference, and strict Bill 96 / Law 25 compliance.

---

## 🗺️ The 4-Pillar Empire

| Pillar | Role | Status |
|--------|------|--------|
| **MAX** | Sovereign Executive / Orchestrator | ✅ Active |
| **Q-MÉTIER** | Service Dispatch & Task Routing | ✅ Active |
| **Q-EMPLOIS** | Tasker Recruitment & Profile Management | ✅ Active |
| **FLOGURU** | Analytics, Forecasting & Vision Layer | 🔜 Coming |

---

## 🧠 4-Tier Intelligence Stack

```
Tier 4 — Vision   │ FLOGURU: market analytics & ARR forecasting
Tier 3 — Worker   │ Task-matching engine (Q-MÉTIER ↔ Q-EMPLOIS)
Tier 2 — Logic    │ dispatch_bridge.py: NL → service type (local LLM)
Tier 1 — Reflex   │ bot.py + lead_logger.py: instant response & logging
```

All LLM inference runs **locally via [Ollama](https://ollama.com)** — zero data leaves your infrastructure. This is the **"Goodbye Tokens"** philosophy: sovereign AI with no per-token cloud billing, no vendor lock-in, and full data residency inside Quebec.

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) running locally with a supported model (default: `mistral`)

```bash
ollama pull mistral
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and set TELEGRAM_BOT_TOKEN (from @BotFather)
```

### 4. Run the bot

```bash
python bot.py
```

---

## 📁 Project Structure

```
MAXIMUS-2.0/
├── bot.py               # Imperial Telegram Bot (Tier 1 & entry point)
├── dispatch_bridge.py   # NL → Service classification via Ollama (Tier 2)
├── lead_logger.py       # CSV / Excel lead logging (Tier 1 Reflex)
├── config.py            # Centralised environment configuration
├── requirements.txt     # Python dependencies
├── .env.example         # Configuration template (safe to commit)
└── data/                # Auto-created lead files (gitignored)
    ├── leads_YYYY-MM-DD.csv
    └── leads_master.xlsx
```

---

## 🤖 Bot Features

### Demander un Service (Dispatch) — Q-MÉTIER
Users describe their need in plain French or English (e.g., *"Mon lavabo fuit"*). The **Tier-2 Logic** layer sends the text to the local Ollama LLM which classifies it into a structured service type (`PLOMBERIE`, `ELECTRICITE`, `NETTOYAGE`, …) and creates a dispatch record.

### Devenir Tasker (Recruitment) — Q-EMPLOIS
Workers register their skills and service zone through a guided conversation. Their profile is logged to the Lead Command dashboard for operator review.

---

## 💰 $50 M ARR Roadmap

| Phase | Milestone | Target |
|-------|-----------|--------|
| **Phase 1** | MVP Bot live, first 500 dispatches | Q1 |
| **Phase 2** | Automated Tasker matching (Tier 3 Worker) | Q2 |
| **Phase 3** | FLOGURU analytics dashboard (Tier 4 Vision) | Q3 |
| **Phase 4** | WhatsApp channel + enterprise B2B accounts | Q4 |
| **Phase 5** | $50 M ARR — Provincial expansion + SaaS licensing | Year 2 |

---

## 🔐 "Goodbye Tokens" — Digital Sovereignty

MAXIMUS runs **all AI inference locally** using Ollama. Benefits:

- ✅ **Zero per-token cost** — no OpenAI / Anthropic billing
- ✅ **Data residency in Quebec** — no cross-border data transfer
- ✅ **Air-gap ready** — works with no internet if needed
- ✅ **Model freedom** — swap `mistral`, `llama3`, `phi3` without code changes

---

## ⚖️ Compliance — Bill 96 & Law 25 (Quebec)

| Requirement | Implementation |
|-------------|----------------|
| French-first interface | Bot UI is French by default |
| Informed consent | Consent notice shown at `/start` (configurable via `CONSENT_TEXT` in `.env`) |
| Data minimisation | Only necessary fields logged (user ID, action, service type) |
| Right to erasure | Lead CSV/Excel files are operator-controlled and deletable |
| Local data residency | LLM inference + lead storage remain on-premise |

---

## 📄 License

See [LICENSE](LICENSE).
