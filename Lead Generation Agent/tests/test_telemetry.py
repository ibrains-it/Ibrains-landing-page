# tests/test_telemetry.py
import unittest
from src.telemetry.analytics import calculate_revenue_per_100_leads, calculate_campaign_funnel_telemetry
from src.scoring.model_governance import propose_scoring_model_update, approve_scoring_model_update

class TestTelemetryModule(unittest.TestCase):
    def test_calculate_revenue_per_100_leads(self):
        rev = calculate_revenue_per_100_leads(qualified_leads_count=50, total_revenue_generated=25000.0)
        self.assertEqual(rev, 50000.0)

    def test_calculate_campaign_funnel_telemetry(self):
        interactions = [
            {"sentiment": "POSITIVE"},
            {"sentiment": "DEMO_REQUESTED"},
            {"sentiment": "CONVERTED", "deal_value": 15000.0},
            {"sentiment": "NEUTRAL"}
        ]
        res = calculate_campaign_funnel_telemetry(interactions)
        self.assertEqual(res["total_interactions"], 4)
        self.assertEqual(res["positive_replies"], 3)
        self.assertEqual(res["total_revenue"], 15000.0)

    def test_model_governance(self):
        telemetry = {"positive_reply_rate_pct": 22.5}
        prop = propose_scoring_model_update("V1.0", telemetry)
        self.assertEqual(prop["proposed_version"], "V2.0")
        self.assertEqual(prop["status"], "PROPOSED_PENDING_HUMAN_APPROVAL")
        
        approved = approve_scoring_model_update(prop, "Head of Growth")
        self.assertEqual(approved["status"], "ACTIVE")
        self.assertEqual(approved["approved_by"], "Head of Growth")

if __name__ == "__main__":
    unittest.main()
