# src/outreach/personalization.py
from typing import Dict, Any, List, Optional

def generate_evidence_backed_outreach(contact: dict, intelligence: dict, agent_catalog_item: dict) -> dict:
    """
    Generates evidence-backed outbound copy for a target decision-maker.
    Mandatorily cites verified evidence to prevent AI hallucinations.
    """
    contact_name = contact.get("name", "Team")
    first_name = contact_name.split()[0] if contact_name else "there"
    org_name = intelligence.get("organization", {}).get("name", "your company")
    agent_name = agent_catalog_item.get("name", "IBrains AI Agent")
    
    evidence_list = intelligence.get("evidence", [])
    evidence_text = evidence_list[0].get("evidence_text", "") if evidence_list else ""
    evidence_url = evidence_list[0].get("source_url", "") if evidence_list else ""

    citation_sentence = f"I noticed on {evidence_url or 'your website'} that {evidence_text[:120]}..." if evidence_text else f"I was reviewing {org_name}'s recent operations..."

    subject = f"AI Automation idea for {org_name}"
    
    body = (
        f"Hi {first_name},\n\n"
        f"{citation_sentence}\n\n"
        f"At IBrains, we've developed the **{agent_name}** to help engineering and operations teams automate candidate screening and customer intake without adding headcount.\n\n"
        f"Would you be open to a quick 10-minute discovery call or a brief live demo?\n\n"
        f"Best regards,\n"
        f"IBrains AI Solutions Team\n"
        f"WhatsApp: +91 9390425742 | Email: ibrains.it@gmail.com"
    )

    return {
        "contact_id": contact.get("id"),
        "contact_email": contact.get("email"),
        "subject": subject,
        "message_body": body,
        "evidence_citation": evidence_text,
        "evidence_url": evidence_url,
        "status": "PENDING_APPROVAL"
    }
