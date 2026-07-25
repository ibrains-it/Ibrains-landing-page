# tests/test_apify_client.py
import unittest
from src.discovery.apify_client import parse_apify_contact_results, calculate_decision_maker_score

class TestApifyClient(unittest.TestCase):
    def test_calculate_decision_maker_score(self):
        self.assertEqual(calculate_decision_maker_score("Chief Executive Officer"), 95)
        self.assertEqual(calculate_decision_maker_score("VP of Talent Acquisition"), 85)
        self.assertEqual(calculate_decision_maker_score("Head of Operations"), 70)

    def test_parse_apify_contact_results(self):
        raw = [
            {
                "name": "Sarah Jenkins",
                "title": "Head of Talent Acquisition",
                "email": "sarah@apexstaffing.com",
                "is_verified": True
            }
        ]
        contacts = parse_apify_contact_results(raw, "org-uuid-123")
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]["email"], "sarah@apexstaffing.com")
        self.assertEqual(contacts[0]["decision_maker_score"], 85)

if __name__ == "__main__":
    unittest.main()
