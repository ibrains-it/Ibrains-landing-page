# src/intelligence/research_agent.py
import hashlib
from typing import Dict, Any, List
from src.intelligence.signal_engine import detect_buying_signals

def generate_evidence_hash(source_url: str, text: str) -> str:
    """Computes SHA-256 hash of evidence string for deduplication."""
    raw = f"{source_url}|{text.strip()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def execute_prospect_research(org_data: dict, page_contents: List[dict]) -> dict:
    """
    Executes deep prospect research across scraped page contents,
    detects buying signals, builds explicit evidence records, and compiles
    the standardized JSON intelligence payload.
    """
    all_signals = []
    all_evidence = []

    for page in page_contents:
        url = page.get("url", org_data.get("website", ""))
        text = page.get("text", "")
        
        # Detect signals on page
        signals = detect_buying_signals(text, meta_data={"url": url, "review_count": org_data.get("review_count", 0)})
        all_signals.extend(signals)
        
        # Construct verified evidence record if relevant text snippet exists
        if len(text.strip()) > 20:
            snippet = text.strip()[:300]
            evidence_hash = generate_evidence_hash(url, snippet)
            all_evidence.append({
                "source_type": page.get("source_type", "WEBSITE_PAGE"),
                "source_url": url,
                "evidence_text": snippet,
                "content_hash": evidence_hash,
                "confidence": 0.92
            })

    # Select recommended agent slug
    candidate_slug = org_data.get("candidate_agent_slug") or "custom-engineering"
    if any(s.get("signal_type") == "HIRING_SPIKE" for s in all_signals):
        candidate_slug = "resume-shortlisting-agent"
    elif any(s.get("signal_type") == "HIGH_REVIEWS_VOLUME" for s in all_signals):
        candidate_slug = "real-estate-voice-agent"

    return {
        "organization": {
            "name": org_data.get("business_name") or org_data.get("name"),
            "domain": org_data.get("normalized_domain") or org_data.get("website"),
            "industry": org_data.get("category", "General")
        },
        "signals": all_signals,
        "evidence": all_evidence,
        "matched_agent_slug": candidate_slug
    }
