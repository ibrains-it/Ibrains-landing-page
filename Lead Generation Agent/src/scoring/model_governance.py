# src/scoring/model_governance.py
from typing import Dict, Any, Optional

def propose_scoring_model_update(current_version: str, telemetry_data: dict) -> dict:
    """
    Analytics Agent recommendation generator:
    Proposes versioned scoring model adjustments (e.g. V1 -> V2) based on campaign telemetry.
    Does NOT auto-apply: requires explicit human approval.
    """
    version_parts = current_version.replace("V", "").split(".")
    major = int(version_parts[0]) if version_parts else 1
    next_version = f"V{major + 1}.0"

    positive_reply_rate = telemetry_data.get("positive_reply_rate_pct", 0)

    # Propose weight rebalancing based on actual conversion signals
    proposed_weights = {
        "icp_weight": 25,
        "pain_weight": 25 if positive_reply_rate > 15 else 20,
        "intent_weight": 25 if positive_reply_rate > 20 else 20,
        "access_weight": 15,
        "value_weight": 10,
        "evidence_weight": 10
    }

    return {
        "current_version": current_version,
        "proposed_version": next_version,
        "status": "PROPOSED_PENDING_HUMAN_APPROVAL",
        "proposed_weights": proposed_weights,
        "justification": f"Based on positive reply rate of {positive_reply_rate}%, rebalancing pain and intent weights."
    }

def approve_scoring_model_update(proposal: dict, approver_name: str) -> dict:
    """
    Human approval gate for scoring model configuration changes.
    Activates the new version (e.g. V2.0).
    """
    return {
        **proposal,
        "status": "ACTIVE",
        "approved_by": approver_name
    }
