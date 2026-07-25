# Implementation Plan & Execution Roadmap (15-Day MVP)
## IBrains Autonomous AI SDR & Revenue Intelligence Platform
**Document Version:** 2.1.0  
**Target Folder:** `Lead Generation Agent/`  
**Date:** July 25, 2026  

---

## 1. Subagent & Skill Assignment Matrix

To maximize execution efficiency, tasks are assigned to specialized subagents and required skills:

| Task ID | Component / Task Description | Assigned Subagent | Required Skill / Tool | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TASK-101** | Execute Supabase `schema_v2_1.sql` & seed `agent_catalog` | `self` (Backend Agent) | PostgreSQL / Supabase Client | ⏳ Pending |
| **TASK-102** | Implement Domain & Entity Normalizer (`normalizer.py`) | `self` (Backend Agent) | Python string normalizers | ⏳ Pending |
| **TASK-103** | Deploy `gosom/google-maps-scraper` Adapter | `research` (Discovery Agent) | Go / Docker / HTTP Runner | ⏳ Pending |
| **TASK-104** | Build Apify Decision Maker Scraper (`apify_client.py`) | `research` (Discovery Agent) | `apify/agent-skills` | ⏳ Pending |
| **TASK-105** | Build Signal Engine & Pre-Outreach Research Agent | `self` (AI Intelligence) | Claude Code / LLM API | ⏳ Pending |
| **TASK-106** | Implement Dynamic Skill Router (`skill_router.py`) | `self` (AI Intelligence) | `sales-skills/sales` | ⏳ Pending |
| **TASK-107** | Build Multi-Factor Lead Scorer (`lead_scorer.py`) | `self` (Backend Agent) | Python / Math Engine | ⏳ Pending |
| **TASK-108** | Implement Human Approval Queue API & Staging | `self` (Backend Agent) | FastAPI / Supabase | ⏳ Pending |
| **TASK-109** | Build Compliance & Suppression Enforcer (`suppression.py`) | `self` (Security Agent) | Python / SQL Indexes | ⏳ Pending |
| **TASK-110** | Wire n8n Workflow JSON Specifications | `self` (Orchestrator) | `Jharilela/n8n-workflows` | ⏳ Pending |
| **TASK-111** | Connect Outbound to FastAPI WhatsApp AI Sales Agent | `self` (Outbound Agent) | FastAPI / Meta Cloud API | ⏳ Pending |
| **TASK-112** | Implement Telemetry & Model Governance Loop | `self` (Analytics Agent) | Revenue & Reply Analytics | ⏳ Pending |

---

## 2. 15-Day Phase-by-Phase Roadmap

### Phase 1: Foundation, Schema Migration & Deduplication (Days 1–3)
- **Goal**: Establish relational persistence, seed official IBrains agent catalog, and implement deduplication.
- **Tasks**:
  1. Execute `schema_v2_1.sql` on Supabase database.
  2. Seed `agent_catalog` with all 11 IBrains live agents (HR Voice Agent, Resume Shortlisting Agent, Technical Interviewer, Real Estate, Ortho Medical, Loan, Insurance, EduFlex).
  3. Implement `normalizer.py` for canonical domain and business name resolution.

### Phase 2: Multi-Source Discovery, Signal Engine & Research Agent (Days 4–6)
- **Goal**: Mine leads from Google Maps and job postings, detect hiring triggers, and generate verified evidence.
- **Tasks**:
  1. Wire `gosom/google-maps-scraper` runner to output normalized payloads.
  2. Implement `signal_engine.py` for hiring spike and workflow friction detection.
  3. Deploy `research_agent.py` to produce JSON intelligence objects with `evidence_url` and `evidence_text`.

### Phase 3: Skill Router, Lead Scorer & Human Approval Queue (Days 7–9)
- **Goal**: Inject targeted sales skills dynamically, score leads (0–100), and stage outreach in human approval queue.
- **Tasks**:
  1. Build `skill_router.py` to inject `prospect-research`, `outbound-copy`, and `roi-calculator`.
  2. Implement 6-factor `lead_scorer.py` algorithm (ICP, Pain, Intent, Access, Value, Evidence).
  3. Build Human Approval staging UI/API (`outreach_messages_v2` with `PENDING_APPROVAL` status).

### Phase 4: Compliance, Deliverability & WhatsApp Outbound Integration (Days 10–12)
- **Goal**: Enforce strict suppression checking, SPF/DKIM/DMARC deliverability, and connect WhatsApp AI Sales Agent.
- **Tasks**:
  1. Build `suppression.py` to block opt-outs, bounces, competitors, and existing clients.
  2. Configure SMTP deliverability headers and bounce handlers.
  3. Connect approved outreach directly to **FastAPI WhatsApp AI Sales Agent** (`d:\IBRAINS\Company Page\Whatsapp Agent`).

### Phase 5: Telemetry, Revenue Tracking & Scoring Governance (Days 13–15)
- **Goal**: Track positive replies, demos, and revenue per 100 leads, establishing human-governed scoring model updates.
- **Tasks**:
  1. Deploy `analytics.py` to calculate Revenue per 100 Qualified Leads.
  2. Implement `scoring_models` versioning (`V1` ➔ `V2`) with human approval gates.

---

## 3. Verification Commands & Unit Testing

```bash
# 1. Test Domain Normalizer & Canonical Deduplication
pytest tests/test_normalizer.py

# 2. Test Signal Engine & Evidence Generation
pytest tests/test_signal_engine.py

# 3. Test Dynamic Skill Router Loading
pytest tests/test_skill_router.py

# 4. Test Compliance & Suppression Engine
pytest tests/test_suppression.py
```
