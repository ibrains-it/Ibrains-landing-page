# src/compliance/suppression.py
from typing import Tuple, List, Optional

# Default in-memory competitor domain blocklist
BLOCKED_DOMAINS = [
    "competitor.com",
    "spamdomain.org",
    "invalid.com",
    "test.com"
]

def is_suppressed(identifier: str, database_suppression_list: Optional[List[dict]] = None) -> Tuple[bool, str]:
    """
    Verifies if an email address, phone number, or domain is suppressed.
    Returns (is_suppressed_bool, reason_string).
    """
    if not identifier:
        return True, "INVALID_IDENTIFIER"

    clean_id = identifier.strip().lower()

    # 1. Check in-memory domain blocklist
    for blocked in BLOCKED_DOMAINS:
        if clean_id == blocked or clean_id.endswith(f".{blocked}") or clean_id.endswith(f"@{blocked}"):
            return True, "COMPETITOR"

    # 2. Check Database Suppression List if provided
    if database_suppression_list:
        for entry in database_suppression_list:
            db_id = (entry.get("identifier") or "").strip().lower()
            if db_id and (clean_id == db_id or clean_id.endswith(f"@{db_id}")):
                return True, entry.get("reason", "OPT_OUT")

    return False, "CLEARED"
