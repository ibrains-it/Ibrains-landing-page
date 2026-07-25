# tests/test_signal_engine.py
import unittest
from src.intelligence.signal_engine import detect_buying_signals
from src.intelligence.research_agent import execute_prospect_research

class TestSignalEngine(unittest.TestCase):
    def test_detect_buying_signals(self):
        text = "We are currently hiring recruiters to manage 1,000+ monthly candidate applications."
        signals = detect_buying_signals(text, meta_data={"url": "https://apexstaffing.com/careers", "review_count": 120})
        
        self.assertGreaterEqual(len(signals), 2)
        signal_types = [s["signal_type"] for s in signals]
        self.assertIn("HIRING_SPIKE", signal_types)
        self.assertIn("HIGH_REVIEWS_VOLUME", signal_types)

    def test_execute_prospect_research(self):
        org_data = {
            "business_name": "Apex Staffing Solutions",
            "normalized_domain": "apexstaffing.com",
            "category": "Recruitment",
            "review_count": 120
        }
        page_contents = [
            {
                "url": "https://apexstaffing.com/careers",
                "text": "We are currently hiring recruiters to process high volume candidate applications."
            }
        ]
        res = execute_prospect_research(org_data, page_contents)
        self.assertEqual(res["organization"]["domain"], "apexstaffing.com")
        self.assertEqual(res["matched_agent_slug"], "resume-shortlisting-agent")
        self.assertGreaterEqual(len(res["evidence"]), 1)

if __name__ == "__main__":
    unittest.main()
