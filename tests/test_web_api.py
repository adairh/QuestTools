"""Tests for the FastAPI web layer."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from questtools.repository import QuestRepository
from questtools.web import create_app


class WebApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.tmpdir.name) / "quests.json"
        self.repository = QuestRepository(self.data_path)
        self.client = TestClient(create_app(self.repository, data_path=self.data_path))

    def tearDown(self) -> None:
        self.client.close()
        self.tmpdir.cleanup()

    def test_document_crud_flow(self) -> None:
        response = self.client.get("/api/document")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["quests"], [])

        create_resp = self.client.post("/api/quests", json={"title": "Quest A"})
        self.assertEqual(create_resp.status_code, 201)
        quest = create_resp.json()
        self.assertEqual(quest["title"], "Quest A")

        quest_id = quest["id"]
        update_resp = self.client.put(
            f"/api/quests/{quest_id}",
            json={"title": "Quest A+", "targets": ["Do X"]},
        )
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(update_resp.json()["targets"], ["Do X"])

        document_update = self.client.put(
            "/api/document",
            json={"title": "Story", "overview": "Mô tả"},
        )
        self.assertEqual(document_update.status_code, 200)
        self.assertEqual(document_update.json()["title"], "Story")

        delete_resp = self.client.delete(f"/api/quests/{quest_id}")
        self.assertEqual(delete_resp.status_code, 204)

        final_resp = self.client.get("/api/document")
        self.assertEqual(final_resp.status_code, 200)
        self.assertEqual(final_resp.json()["quests"], [])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
