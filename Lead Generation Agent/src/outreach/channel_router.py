# src/outreach/channel_router.py
from typing import Dict, Any

def select_optimal_channel(contact: dict, interaction_history: list = None) -> str:
    """
    Channel Strategy Router: Selects optimal initial channel (EMAIL vs WHATSAPP vs LINKEDIN)
    and handles sequential channel escalations based on interaction history.
    """
    interaction_history = interaction_history or []

    # 1. If previous WhatsApp conversation exists, continue on WhatsApp
    if any(i.get("channel") == "WHATSAPP" for i in interaction_history):
        return "WHATSAPP"

    # 2. If verified executive email exists, default to Email
    if contact.get("email_verified") or contact.get("email"):
        return "EMAIL"

    # 3. If direct phone / WhatsApp opt-in exists, route to WhatsApp
    if contact.get("phone"):
        return "WHATSAPP"

    return "LINKEDIN"
