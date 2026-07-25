# tests/test_lead_scorer.py
import unittest
from src.scoring.lead_scorer import calculate_lead_score

class TestLeadScorer(unittest.TestCase):
    def test_calculate_lead_score_hot(self):
        org = {"industry": "Recruiting & Staffing", "employee_range": "50-200", "review_count": 120}
        signals = [{"signal_type": "HIRING_SPIKE"}, {"signal_type": "HIGH_REVIEWS_VOLUME"}]
        evidence = [{"confidence": 0.95}]
        contacts = [{"email_verified": True}]
        
        score = calculate_lead_score(org, signals, evidence, contacts)
        self.assertGreaterEqual(score["total_score"], 85)
        self.assertEqual(score["priority"], "HOT")

    def test_calculate_lead_score_nurture(self):
        org = {"industry": "Consulting"}
        signals = []
        evidence = []
        contacts = []
        
        score = calculate_lead_score(org, signals, evidence, contacts)
        self.assertLess(score["total_score"], 70)
        self.assertIn(score["priority"], ["NURTURE", "IGNORE"])

if __name__ == "__main__":
    unittest.main()
