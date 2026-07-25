# tests/test_skill_router.py
import unittest
from src.intelligence.skill_router import resolve_skill_by_intent, get_skill_instruction

class TestSkillRouter(unittest.TestCase):
    def test_resolve_skill_by_intent(self):
        self.assertIn("geo-content", resolve_skill_by_intent("research"))
        self.assertIn("geo-proposal", resolve_skill_by_intent("proposal"))
        self.assertIn("geo-schema", resolve_skill_by_intent("schema"))
        self.assertIn("geo-audit", resolve_skill_by_intent("audit"))

    def test_get_skill_instruction(self):
        res = get_skill_instruction("proposal")
        self.assertEqual(res["intent"], "proposal")
        self.assertIn("instructions", res)

if __name__ == "__main__":
    unittest.main()
