# src/discovery/normalizer.py
import re
import hashlib
from urllib.parse import urlparse
from typing import Optional

# Multi-word suffixes must be listed BEFORE single-word suffixes to match completely
CORPORATE_SUFFIXES = [
    r'\bprivate limited\b',
    r'\bpvt\.?\s*ltd\.?\b',
    r'\bpty\.?\s*ltd\.?\b',
    r'\blimited liability company\b',
    r'\binc\.?\b', r'\bincorporated\b',
    r'\bllc\.?\b', r'\bltd\.?\b', r'\blimited\b',
    r'\bcorp\.?\b', r'\bcorporation\b',
    r'\bco\.?\b', r'\bcompany\b',
    r'\bgroup\b', r'\bholdings\b', r'\bservices\b'
]

def normalize_domain(raw_input: Optional[str]) -> Optional[str]:
    """
    Strips URL schemes, www prefixes, paths, and query strings to produce
    a clean canonical domain name.
    """
    if not raw_input:
        return None

    clean = raw_input.strip().lower()
    
    if not clean.startswith(("http://", "https://")):
        clean = "http://" + clean
        
    try:
        parsed = urlparse(clean)
        host = parsed.netloc or parsed.path
    except Exception:
        return None

    host = host.split(":")[0]
    if host.startswith("www."):
        host = host[4:]
        
    return host if host else None

def normalize_company_name(name: Optional[str]) -> str:
    """
    Strips corporate suffixes, special punctuation, and extra spaces
    to produce a canonical company name for entity resolution.
    """
    if not name:
        return ""

    clean = name.strip()
    
    for pattern in CORPORATE_SUFFIXES:
        clean = re.sub(pattern, "", clean, flags=re.IGNORECASE)
        
    clean = re.sub(r'[^\w\s]', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    return clean

def generate_dedupe_hash(domain: Optional[str], company_name: Optional[str]) -> str:
    """
    Generates a deterministic SHA-256 hash for deduplication based on canonical domain and name.
    """
    norm_domain = normalize_domain(domain) or ""
    norm_name = normalize_company_name(company_name).lower()
    
    raw_key = f"{norm_domain}|{norm_name}".encode("utf-8")
    return hashlib.sha256(raw_key).hexdigest()

def process_lead_payload(payload: dict) -> dict:
    """
    Enriches a raw lead payload with canonical normalized domain, name, and dedupe hash.
    """
    raw_website = payload.get("website") or payload.get("url") or ""
    raw_name = payload.get("business_name") or payload.get("name") or ""
    
    norm_domain = normalize_domain(raw_website)
    norm_name = normalize_company_name(raw_name)
    dedupe_hash = generate_dedupe_hash(norm_domain, norm_name)
    
    return {
        **payload,
        "normalized_domain": norm_domain,
        "normalized_name": norm_name,
        "dedupe_hash": dedupe_hash
    }
