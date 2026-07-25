# src/discovery/google_maps.py
import json
import logging
from typing import List, Dict, Any
from src.discovery.normalizer import process_lead_payload

logger = logging.getLogger(__name__)

# Keyword map for initial agent matching based on business category
CATEGORY_AGENT_MAP = {
    "real estate": "real-estate-voice-agent",
    "realty": "real-estate-voice-agent",
    "property management": "real-estate-voice-agent",
    "recruitment": "hr-voice-agent",
    "staffing": "resume-shortlisting-agent",
    "hr consultant": "hr-voice-agent",
    "medical clinic": "ortho-medical-agent",
    "orthopedic": "ortho-medical-agent",
    "hospital": "ortho-medical-agent",
    "bank": "loan-agent",
    "mortgage": "loan-agent",
    "lender": "loan-agent",
    "insurance": "insurance-agent",
    "school": "eduflex-platform",
    "academy": "eduflex-platform",
    "software": "technical-interviewer-agent",
    "it services": "coding-round-interviewer-agent"
}

def match_agent_by_category(category: str) -> str:
    """Matches a business category string to a candidate IBrains agent slug."""
    if not category:
        return "custom-engineering"
    cat_lower = category.lower()
    for kw, agent_slug in CATEGORY_AGENT_MAP.items():
        if kw in cat_lower:
            return agent_slug
    return "custom-engineering"

def parse_maps_scraper_output(raw_json_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ingests raw JSON outputs from gosom/google-maps-scraper,
    runs domain/name normalization, generates dedupe hash, and attaches matched agent slug.
    """
    processed_leads = []
    
    for item in raw_json_data:
        # Extract fields from gosom JSON output schema
        business_name = item.get("title") or item.get("name") or ""
        website = item.get("website") or item.get("web") or ""
        phone = item.get("phone") or item.get("telephone") or ""
        address = item.get("address") or ""
        category = item.get("category") or item.get("type") or ""
        rating = float(item.get("review_rating") or item.get("rating") or 0.0)
        review_count = int(item.get("review_count") or item.get("reviews") or 0)
        
        if not business_name:
            continue
            
        base_lead = {
            "source_platform": "GOOGLE_MAPS",
            "source_external_id": item.get("place_id") or item.get("id") or "",
            "business_name": business_name,
            "website": website,
            "phone": phone,
            "address": address,
            "category": category,
            "rating": rating,
            "review_count": review_count,
            "candidate_agent_slug": match_agent_by_category(category)
        }
        
        # Run through normalizer
        normalized_lead = process_lead_payload(base_lead)
        processed_leads.append(normalized_lead)
        
    return processed_leads
