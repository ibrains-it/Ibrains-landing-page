# src/discovery/apify_client.py
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def calculate_decision_maker_score(job_title: str) -> int:
    """Calculates decision-maker score (0-100) based on seniority in title."""
    if not job_title:
        return 50
    title_upper = job_title.upper()
    if any(t in title_upper for t in ["CEO", "FOUNDER", "CHIEF EXECUTIVE", "OWNER"]):
        return 95
    if any(t in title_upper for t in ["CTO", "HEAD OF TALENT", "HEAD OF RECRUITING", "HEAD OF HR", "VP OF TALENT", "DIRECTOR"]):
        return 85
    if any(t in title_upper for t in ["VP", "HEAD OF", "MANAGER"]):
        return 70
    return 50

def parse_apify_contact_results(raw_apify_items: List[Dict[str, Any]], organization_id: str) -> List[Dict[str, Any]]:
    """
    Ingests raw output items from Apify enrichment actors,
    extracts decision-maker contact details, calculates decision-maker scores,
    and returns standardized contact objects for DB persistence.
    """
    contacts = []
    seen_emails = set()
    
    for item in raw_apify_items:
        email = (item.get("email") or item.get("work_email") or "").strip().lower()
        if not email or email in seen_emails:
            continue
            
        name = item.get("name") or f"{item.get('first_name', '')} {item.get('last_name', '')}".strip() or "Executive Contact"
        job_title = item.get("title") or item.get("job_title") or item.get("headline") or "Decision Maker"
        phone = item.get("phone") or item.get("direct_phone") or ""
        linkedin_url = item.get("linkedin_url") or item.get("profile_url") or ""
        email_verified = bool(item.get("is_verified") or item.get("email_status") == "valid")
        
        score = calculate_decision_maker_score(job_title)
        
        seen_emails.add(email)
        contacts.append({
            "organization_id": organization_id,
            "name": name,
            "job_title": job_title,
            "email": email,
            "email_verified": email_verified,
            "phone": phone,
            "linkedin_url": linkedin_url,
            "decision_maker_score": score
        })
        
    return contacts
