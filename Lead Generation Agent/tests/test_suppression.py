# tests/test_suppression.py
import unittest
from src.compliance.suppression import is_suppressed

class TestSuppression(unittest.TestCase):
    def test_is_suppressed_blocked_domain(self):
        suppressed, reason = is_suppressed("john@competitor.com")
        self.assertTrue(suppressed)
        self.assertEqual(reason, "COMPETITOR")

    def test_is_suppressed_cleared(self):
        suppressed, reason = is_suppressed("sarah@apexstaffing.com")
        self.assertFalse(suppressed)
        self.assertEqual(reason, "CLEARED")

    def test_is_suppressed_db_list(self):
        db_list = [{"identifier": "optout@example.com", "reason": "OPT_OUT"}]
        suppressed, reason = is_suppressed("optout@example.com", database_suppression_list=db_list)
        self.assertTrue(suppressed)
        self.assertEqual(reason, "OPT_OUT")

if __name__ == "__main__":
    unittest.main()
