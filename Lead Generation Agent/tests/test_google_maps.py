# tests/test_google_maps.py
import unittest
from src.discovery.google_maps import parse_maps_scraper_output, match_agent_by_category

class TestGoogleMapsAdapter(unittest.TestCase):
    def test_match_agent_by_category(self):
        self.assertEqual(match_agent_by_category("Real Estate Agency"), "real-estate-voice-agent")
        self.assertEqual(match_agent_by_category("Recruitment & HR"), "hr-voice-agent")
        self.assertEqual(match_agent_by_category("Orthopedic Clinic"), "ortho-medical-agent")
        self.assertEqual(match_agent_by_category("Software Development"), "technical-interviewer-agent")

    def test_parse_maps_scraper_output(self):
        raw_items = [
            {
                "title": "Apex Staffing Solutions, Inc.",
                "website": "https://www.apexstaffing.com/careers",
                "phone": "+1-555-019-2834",
                "category": "Recruitment Agency",
                "review_rating": 4.8,
                "review_count": 142
            }
        ]
        parsed = parse_maps_scraper_output(raw_items)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["normalized_domain"], "apexstaffing.com")
        self.assertEqual(parsed[0]["candidate_agent_slug"], "hr-voice-agent")

if __name__ == "__main__":
    unittest.main()
