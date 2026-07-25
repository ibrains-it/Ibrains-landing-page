# src/outreach/approval_queue.py
from typing import Dict, Any, List

def stage_message_for_approval(message_payload: dict, staging_queue: List[dict]) -> dict:
    """
    Stages an AI-generated outbound message in the Human Approval Queue.
    Ensures message status is PENDING_APPROVAL.
    """
    staged = {
        **message_payload,
        "status": "PENDING_APPROVAL",
        "approved_by": None
    }
    staging_queue.append(staged)
    return staged

def approve_staged_message(message_id: str, approver_name: str, staging_queue: List[dict]) -> dict:
    """
    Approves a staged message in the Human Approval Queue, transitioning status to APPROVED.
    """
    for msg in staging_queue:
        if msg.get("contact_id") == message_id or msg.get("id") == message_id:
            msg["status"] = "APPROVED"
            msg["approved_by"] = approver_name
            return msg
    return {"error": "Message not found in queue"}
