# tests/test_outreach.py
import unittest
from src.outreach.personalization import generate_evidence_backed_outreach
from src.outreach.channel_router import select_optimal_channel
from src.outreach.approval_queue import stage_message_for_approval, approve_staged_message

class TestOutreachModule(unittest.TestCase):
    def test_generate_evidence_backed_outreach(self):
        contact = {"id": "c1", "name": "Sarah Jenkins", "email": "sarah@apexstaffing.com"}
        intelligence = {
            "organization": {"name": "Apex Staffing Solutions"},
            "evidence": [{"source_url": "https://apexstaffing.com/careers", "evidence_text": "Hiring 8 recruiters"}]
        }
        agent_catalog_item = {"name": "Resume Shortlisting Agent"}
        
        msg = generate_evidence_backed_outreach(contact, intelligence, agent_catalog_item)
        self.assertEqual(msg["status"], "PENDING_APPROVAL")
        self.assertIn("Resume Shortlisting Agent", msg["message_body"])
        self.assertIn("Hiring 8 recruiters", msg["message_body"])

    def test_select_optimal_channel(self):
        contact = {"email": "sarah@apexstaffing.com", "email_verified": True}
        self.assertEqual(select_optimal_channel(contact), "EMAIL")
        
        contact_phone = {"phone": "+15550192834"}
        self.assertEqual(select_optimal_channel(contact_phone), "WHATSAPP")

    def test_approval_queue(self):
        queue = []
        msg = {"id": "msg-101", "contact_id": "c1", "status": "PENDING_APPROVAL"}
        staged = stage_message_for_approval(msg, queue)
        self.assertEqual(len(queue), 1)
        
        approved = approve_staged_message("c1", "IBrains Manager", queue)
        self.assertEqual(approved["status"], "APPROVED")
        self.assertEqual(approved["approved_by"], "IBrains Manager")

if __name__ == "__main__":
    unittest.main()
