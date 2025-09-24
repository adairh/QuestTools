"""Tests for the quest repository layer."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from questtools.repository import QuestRepository


class QuestRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.tmpdir.name) / "quests.json"
        self.repository = QuestRepository(self.data_path)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def _load_raw(self) -> dict:
        if not self.data_path.exists():
            return {}
        return json.loads(self.data_path.read_text(encoding="utf-8"))

    def test_create_update_delete_quest(self) -> None:
        quest = self.repository.create_quest({"title": "Test quest", "targets": ["Do something"]})
        self.assertEqual(quest.title, "Test quest")
        self.assertEqual(quest.targets, ["Do something"])

        quest = self.repository.update_quest(
            quest.id,
            {
                "title": "Updated quest",
                "description": "New description",
                "targets": ["First", "Second"],
                "dialog_accept": ["Xin chào"],
            },
        )
        self.assertEqual(quest.title, "Updated quest")
        self.assertEqual(quest.targets, ["First", "Second"])
        self.assertEqual(quest.dialog_accept, ["Xin chào"])

        self.repository.delete_quest(quest.id)
        data = self._load_raw()
        self.assertEqual(data.get("quests"), [])

    def test_update_document_metadata(self) -> None:
        document = self.repository.update_document(title="Tài liệu", overview="Mô tả")
        self.assertEqual(document.title, "Tài liệu")
        self.assertEqual(document.overview, "Mô tả")

        data = self._load_raw()
        self.assertEqual(data.get("title"), "Tài liệu")
        self.assertEqual(data.get("overview"), "Mô tả")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
