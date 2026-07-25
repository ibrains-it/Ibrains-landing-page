# tests/test_normalizer.py
import unittest
from src.discovery.normalizer import (
    normalize_domain,
    normalize_company_name,
    generate_dedupe_hash,
    process_lead_payload
)

class TestNormalizer(unittest.TestCase):
    def test_normalize_domain(self):
        self.assertEqual(normalize_domain("https://www.apexstaffing.com/about?ref=google"), "apexstaffing.com")
        self.assertEqual(normalize_domain("http://apexstaffing.co.uk/"), "apexstaffing.co.uk")
        self.assertEqual(normalize_domain("www.techcorp.io/careers"), "techcorp.io")
        self.assertEqual(normalize_domain("apexstaffing.com"), "apexstaffing.com")
        self.assertIsNone(normalize_domain(""))
        self.assertIsNone(normalize_domain(None))

    def test_normalize_company_name(self):
        self.assertEqual(normalize_company_name("Apex Staffing Solutions, Inc."), "Apex Staffing Solutions")
        self.assertEqual(normalize_company_name("ABC Private Limited"), "ABC")
        self.assertEqual(normalize_company_name(" Global  Tech  LLC  "), "Global Tech")
        self.assertEqual(normalize_company_name("Real Estate Holdings Group"), "Real Estate")

    def test_generate_dedupe_hash(self):
        hash1 = generate_dedupe_hash("https://www.apexstaffing.com", "Apex Staffing Inc.")
        hash2 = generate_dedupe_hash("apexstaffing.com/contact", "Apex Staffing LLC")
        self.assertEqual(hash1, hash2)

    def test_process_lead_payload(self):
        raw = {
            "business_name": "Apex Staffing Solutions, Inc.",
            "website": "https://www.apexstaffing.com/careers",
            "phone": "+1-555-019-2834"
        }
        processed = process_lead_payload(raw)
        self.assertEqual(processed["normalized_domain"], "apexstaffing.com")
        self.assertEqual(processed["normalized_name"], "Apex Staffing Solutions")
        self.assertIn("dedupe_hash", processed)

if __name__ == "__main__":
    unittest.main()
