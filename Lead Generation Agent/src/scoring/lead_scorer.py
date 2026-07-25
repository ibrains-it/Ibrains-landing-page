# src/scoring/lead_scorer.py
from typing import Dict, Any, List

DEFAULT_SCORING_WEIGHTS = {
    "icp_weight": 25,
    "pain_weight": 20,
    "intent_weight": 20,
    "access_weight": 15,
    "value_weight": 10,
    "evidence_weight": 10
}

TARGET_INDUSTRIES = ["Recruitment", "Staffing", "Real Estate", "Healthcare", "EdTech", "Software", "Finance", "Insurance"]

def calculate_lead_score(org_data: dict, signals: List[dict], evidence: List[dict], contacts: List[dict], custom_weights: dict = None) -> dict:
    """
    Computes a multi-factor 0-100 lead score based on 6 core criteria:
    1. ICP Fit (25 pts)
    2. Pain / Automation Fit (20 pts)
    3. Intent Signal (20 pts)
    4. Decision Maker Access (15 pts)
    5. Potential Business Value (10 pts)
    6. Evidence Quality (10 pts)
    """
    w = custom_weights or DEFAULT_SCORING_WEIGHTS

    # 1. ICP Fit
    industry = org_data.get("industry") or org_data.get("category") or ""
    icp_score = w["icp_weight"] if any(ind.lower() in industry.lower() for ind in TARGET_INDUSTRIES) else 10

    # 2. Pain / Automation Fit
    pain_count = len(signals)
    pain_score = w["pain_weight"] if pain_count >= 2 else (w["pain_weight"] // 2 if pain_count == 1 else 0)

    # 3. Intent Signal
    has_hiring_intent = any(s.get("signal_type") == "HIRING_SPIKE" for s in signals)
    intent_score = w["intent_weight"] if has_hiring_intent else 5

    # 4. Decision Maker Access
    has_verified_email = any(c.get("email_verified") for c in contacts) or bool(contacts)
    access_score = w["access_weight"] if has_verified_email else 5

    # 5. Potential Business Value
    employee_range = org_data.get("employee_range", "")
    review_count = org_data.get("review_count", 0)
    value_score = w["value_weight"] if review_count >= 50 or "50" in employee_range else 5

    # 6. Evidence Quality
    has_high_confidence_evidence = any(e.get("confidence", 0) >= 0.90 for e in evidence)
    evidence_score = w["evidence_weight"] if has_high_confidence_evidence else 2

    total_score = icp_score + pain_score + intent_score + access_score + value_score + evidence_score

    # Determine priority tier
    if total_score >= 85:
        priority = "HOT"
    elif total_score >= 70:
        priority = "HIGH"
    elif total_score >= 50:
        priority = "NURTURE"
    else:
        priority = "IGNORE"

    return {
        "total_score": total_score,
        "priority": priority,
        "breakdown": {
            "icp": icp_score,
            "pain": pain_score,
            "intent": intent_score,
            "access": access_score,
            "value": value_score,
            "evidence": evidence_score
        }
    }
