# src/intelligence/signal_engine.py
import re
from typing import List, Dict, Any, Optional

SIGNAL_PATTERNS = {
    "HIRING_SPIKE": [
        r'\bhiring\b.*?\b(recruiter|recruiters|talent|hr|interviewer)\b',
        r'\bmanaging\b.*?\b(applications|candidates|resumes)\b',
        r'\bhigh volume hiring\b'
    ],
    "HIGH_REVIEWS_VOLUME": [
        r'\b50\+?\s*reviews\b',
        r'\bhigh volume calls\b'
    ],
    "MANUAL_WORKFLOW": [
        r'\bcontact form\b',
        r'\bcall us\b',
        r'\bno automated qualification\b'
    ]
}

def detect_buying_signals(scraped_text: str, meta_data: Optional[dict] = None) -> List[Dict[str, Any]]:
    """
    Scans company careers pages, job descriptions, and website meta data
    to detect buying signals and automation triggers.
    """
    signals = []
    text_lower = scraped_text.lower() if scraped_text else ""
    meta_data = meta_data or {}
    
    # 1. Check Hiring Spike Signal
    for pattern in SIGNAL_PATTERNS["HIRING_SPIKE"]:
        match = re.search(pattern, text_lower)
        if match:
            signals.append({
                "signal_type": "HIRING_SPIKE",
                "description": f"Hiring activity detected around candidate screening: '{match.group(0)}'",
                "source_url": meta_data.get("url", ""),
                "confidence": 0.92
            })
            break

    # 2. Check High Review Volume / Local Business Friction Signal
    review_count = meta_data.get("review_count", 0)
    if review_count >= 50:
        signals.append({
            "signal_type": "HIGH_REVIEWS_VOLUME",
            "description": f"High customer engagement ({review_count} Google reviews) with manual phone handling.",
            "source_url": meta_data.get("url", ""),
            "confidence": 0.88
        })

    # 3. Check Manual Workflow Signal
    if meta_data.get("has_whatsapp") is False or "contact form" in text_lower:
        signals.append({
            "signal_type": "MANUAL_WORKFLOW",
            "description": "Manual intake process with opportunity for real-time AI Voice / WhatsApp Agent.",
            "source_url": meta_data.get("url", ""),
            "confidence": 0.85
        })

    return signals
