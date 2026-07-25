# src/telemetry/analytics.py
from typing import List, Dict, Any

def calculate_revenue_per_100_leads(qualified_leads_count: int, total_revenue_generated: float) -> float:
    """
    Computes primary revenue efficiency metric: Revenue / 100 Qualified Leads.
    """
    if not qualified_leads_count or qualified_leads_count <= 0:
        return 0.0
    return round((total_revenue_generated / qualified_leads_count) * 100, 2)

def calculate_campaign_funnel_telemetry(interactions: List[Dict[str, Any]]) -> dict:
    """
    Calculates campaign telemetry focusing on hard conversion metrics:
    Delivered -> Positive Reply -> Qualified Conversation -> Demo -> Proposal -> Signed Client.
    Excludes unreliable email open metrics.
    """
    total = len(interactions)
    positive_replies = sum(1 for i in interactions if i.get("sentiment") in ["POSITIVE", "DEMO_REQUESTED", "CONVERTED"])
    demos_booked = sum(1 for i in interactions if i.get("sentiment") in ["DEMO_REQUESTED", "CONVERTED"])
    conversions = sum(1 for i in interactions if i.get("sentiment") == "CONVERTED")
    total_deal_value = sum(float(i.get("deal_value", 0)) for i in interactions if i.get("sentiment") == "CONVERTED")

    positive_reply_rate = round((positive_replies / total * 100), 2) if total > 0 else 0.0
    demo_booking_rate = round((demos_booked / total * 100), 2) if total > 0 else 0.0

    return {
        "total_interactions": total,
        "positive_replies": positive_replies,
        "positive_reply_rate_pct": positive_reply_rate,
        "demos_booked": demos_booked,
        "demo_booking_rate_pct": demo_booking_rate,
        "conversions": conversions,
        "total_revenue": total_deal_value,
        "revenue_per_100_leads": calculate_revenue_per_100_leads(total, total_deal_value)
    }
