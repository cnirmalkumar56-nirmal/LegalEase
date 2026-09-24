import importlib
import os
import sys
import unittest

from fastapi.testclient import TestClient


class BackendHealthTest(unittest.TestCase):
    def test_health_works_without_gemini_key(self):
        os.environ.pop("GEMINI_API_KEY", None)
        for module_name in ["backend.routes", "backend.main", "ai_core.gemini_generator"]:
            sys.modules.pop(module_name, None)

        import backend.main

        importlib.reload(backend.main)
        client = TestClient(backend.main.app)

        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_generate_works_without_gemini_key(self):
        os.environ.pop("GEMINI_API_KEY", None)
        for module_name in ["backend.routes", "backend.main", "ai_core.gemini_generator"]:
            sys.modules.pop(module_name, None)

        import backend.main

        importlib.reload(backend.main)
        client = TestClient(backend.main.app)

        response = client.post(
            "/generate",
            json={
                "document_type": "Non-Disclosure Agreement",
                "parties": "Jane Doe, TechNova Inc.",
                "terms": "Confidentiality must be maintained; Payment within 30 days",
                "effective_date": "2026-09-22",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("draft", response.json()["content"].lower())


if __name__ == "__main__":
    unittest.main()
