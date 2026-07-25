# Low-Level Architecture & Design Document (LLD V2.1)
## IBrains Autonomous AI SDR & Revenue Intelligence Platform
**Document Version:** 2.1.0  
**Target Organization:** IBrains AI Engineering Studio  
**Date:** July 25, 2026  
**Status:** APPROVED FOR IMPLEMENTATION  

---

## 1. System Folder & Module Architecture

```text
Lead Generation Agent/
├── HLD_DESIGN_DOCUMENT.md
├── LLD_DESIGN_DOCUMENT.md
├── IMPLEMENTATION_PLAN.md
├── schema_v2_1.sql
├── config/
│   ├── settings.py                # Pydantic environment configuration
│   └── scoring_weights.json       # Versioned scoring weights configuration
├── src/
│   ├── discovery/
│   │   ├── google_maps.py         # gosom scraper runner & parser
│   │   ├── apify_client.py        # Apify decision maker enrichment actor
│   │   ├── job_board_signals.py   # Career site & job posting signal scraper
│   │   └── normalizer.py          # Domain & entity deduplication logic
│   ├── intelligence/
│   │   ├── signal_engine.py       # Intent & buying trigger detector
│   │   ├── research_agent.py      # Pre-outreach research & evidence collector
│   │   └── skill_router.py        # Dynamic skill loader (SKILL.md router)
│   ├── scoring/
│   │   ├── lead_scorer.py         # Multi-factor 0-100 scoring calculator
│   │   └── model_governance.py    # Scoring model versioning & approval
│   ├── outreach/
│   │   ├── personalization.py     # Evidence-backed copy generator
│   │   ├── channel_router.py      # Email / WhatsApp / LinkedIn channel selector
│   │   └── approval_queue.py      # Staging queue & human-in-the-loop triggers
│   ├── compliance/
│   │   ├── suppression.py         # Global opt-out, bounce & competitor checker
│   │   └── deliverability.py      # Rate limiter, SPF/DKIM headers, bounce handler
│   └── telemetry/
│       ├── analytics.py           # Revenue per 100 leads & positive reply tracker
│       └── feedback_loop.py       # Model performance evaluation engine
├── n8n_workflows/
│   ├── 01_lead_ingestion_dedupe.json
│   ├── 02_signal_detection_research.json
│   ├── 03_outreach_approval_queue.json
│   └── 04_channel_dispatch_feedback.json
└── tests/
    ├── test_normalizer.py
    ├── test_signal_engine.py
    ├── test_skill_router.py
    └── test_suppression.py
```

---

## 2. API Contracts & Webhook Payload Specifications

### Endpoint 1: Raw Lead Ingestion & Deduplication
- **Route**: `POST /api/v1/leads/ingest`
- **Request Payload**:
```json
{
  "source_platform": "GOOGLE_MAPS",
  "source_external_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
  "business_name": "Apex Staffing Solutions Inc.",
  "website": "https://www.apexstaffing.com/contact",
  "phone": "+1-555-019-2834",
  "city": "Austin",
  "category": "Recruitment Agency",
  "rating": 4.8,
  "review_count": 142
}
```
- **Response Payload**:
```json
{
  "status": "INGESTED",
  "organization_id": "9b1deb4d-3b7d-41b6-91d7-2c67f70b4a12",
  "normalized_domain": "apexstaffing.com",
  "is_duplicate": false
}
```

### Endpoint 2: Pre-Outreach Research & Multi-Evidence Gathering
- **Route**: `POST /api/v1/research/analyze`
- **Request Payload**: `{ "organization_id": "9b1deb4d-3b7d-41b6-91d7-2c67f70b4a12" }`
- **Response Payload**:
```json
{
  "organization_id": "9b1deb4d-3b7d-41b6-91d7-2c67f70b4a12",
  "matched_agent_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "matched_agent_slug": "resume-shortlisting-agent",
  "lead_score": 92,
  "priority": "HOT",
  "evidence": [
    {
      "source_url": "https://apexstaffing.com/careers/senior-recruiter",
      "evidence_text": "Seeking 6 Senior Recruiters to manage 1,500 monthly applicant profiles.",
      "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "confidence": 0.95
    }
  ]
}
```

---

## 3. Dynamic Skill Router Implementation Contract

The **Skill Router** dynamically injects the precise skill instruction package based on workflow phase:

```python
# src/intelligence/skill_router.py

import os
from typing import Dict

SKILLS_REGISTRY = {
    "RESEARCH": "skills/prospect-research/SKILL.md",
    "OUTBOUND_COPY": "skills/outbound-copy/SKILL.md",
    "ROI_CALCULATOR": "skills/roi-calculator/SKILL.md",
    "PROPOSAL": "skills/geo-proposal/SKILL.md",
    "LEGAL": "skills/legal-contracts/SKILL.md"
}

def load_skill_prompt(phase: str) -> str:
    skill_path = SKILLS_REGISTRY.get(phase.upper())
    if not skill_path or not os.path.exists(skill_path):
        raise ValueError(f"Unknown or missing skill package for phase: {phase}")
    
    with open(skill_path, "r", encoding="utf-8") as f:
        return f.read()
```

---

## 4. Multi-Factor Scoring Formula Algorithm

$$\text{Lead Score} = \text{ICP} + \text{Pain} + \text{Intent} + \text{Access} + \text{Value} + \text{Evidence}$$

```python
# src/scoring/lead_scorer.py

def calculate_lead_score(org_data: dict, signals: list, evidence: list, weights: dict) -> dict:
    icp_score = 25 if org_data.get("industry") in ["Recruitment", "Real Estate", "Healthcare", "EdTech"] else 10
    pain_score = 20 if len(signals) >= 2 else (10 if len(signals) == 1 else 0)
    intent_score = 20 if any(s.get("type") == "HIRING_SPIKE" for s in signals) else 5
    access_score = 15 if org_data.get("email_verified") else 5
    value_score = 10 if org_data.get("employee_range") in ["50-200", "200-500", "500+"] else 5
    evidence_score = 10 if any(e.get("confidence", 0) >= 0.90 for e in evidence) else 2

    total_score = icp_score + pain_score + intent_score + access_score + value_score + evidence_score
    
    priority = "HOT" if total_score >= 85 else ("HIGH" if total_score >= 70 else "NURTURE")
    
    return {
        "total_score": total_score,
        "priority": priority,
        "breakdown": {
            "icp": icp_score, "pain": pain_score, "intent": intent_score,
            "access": access_score, "value": value_score, "evidence": evidence_score
        }
    }
```

---

## 5. Compliance & Suppression Enforcer

Before dispatching any outbound email or WhatsApp message, the `suppression.py` module executes 4 strict checks:

```python
# src/compliance/suppression.py

def is_suppressed(identifier: str, supabase_client) -> tuple[bool, str]:
    # 1. Clean identifier
    clean_id = identifier.strip().lower()
    
    # 2. Check global suppression list
    res = supabase_client.table("suppression_list").select("reason").eq("identifier", clean_id).execute()
    if res.data:
        return True, res.data[0]["reason"]
    
    # 3. Check competitor domain block
    if any(clean_id.endswith(domain) for domain in ["competitor.com", "spamdomain.org"]):
        return True, "COMPETITOR"

    return False, "CLEARED"
```

---

## 6. n8n Node Workflow Specifications

### Workflow 1: `01_lead_ingestion_dedupe.json`
1. **Webhook Node**: Receives JSON payload from scraper adapters.
2. **Function Node (Normalizer)**: Strips URL schemes, normalizes company names.
3. **Supabase Node**: Executes upsert into `organizations_v2` and `lead_sources`.
4. **Router Node**: If new lead ➔ Triggers `02_signal_detection_research.json`.

### Workflow 2: `03_outreach_approval_queue.json`
1. **Supabase Poller Node**: Queries `opportunities_v2` where `priority = 'HOT'`.
2. **Claude Code Node**: Injects `outbound-copy` skill and generates message with evidence citation.
3. **Supabase Node**: Inserts message into `outreach_messages_v2` with `status = 'PENDING_APPROVAL'`.
4. **Slack / Telegram Notification Node**: Alerts IBrains sales team: *"New HOT Lead ready for 1-click approval!"*
