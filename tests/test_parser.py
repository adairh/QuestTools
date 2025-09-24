import unittest
from pathlib import Path

from questtools.parser import parse_document


class ParserIntegrationTest(unittest.TestCase):
    DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "tan_thu.txt"

    def test_parse_document_creates_expected_quests(self) -> None:
        text = self.DATA_PATH.read_text(encoding="utf-8")
        document = parse_document(text)

        self.assertEqual(document.title, "Cốt truyện và Nhiệm vụ Tân thủ")
        self.assertEqual(len(document.quests), 30)

        first = document.quests[0]
        self.assertEqual(first.title, "Rừng tre ban sớm")
        self.assertIn("Vác rìu đi vào rừng tre", first.description)
        self.assertEqual(first.accept_npc, "(Auto - mở màn)")
        self.assertTrue(first.dialog_accept)
        self.assertTrue(first.targets)

        last = document.quests[-1]
        self.assertEqual(last.title, "Những ngày chuẩn bị")
        self.assertTrue("luyện côn" in " ".join(last.notes) or last.description is None)

    def test_conversion_to_json_structure(self) -> None:
        text = self.DATA_PATH.read_text(encoding="utf-8")
        document = parse_document(text)
        payload = document.to_dict()

        self.assertIn("overview", payload)
        self.assertIn("quests", payload)
        self.assertEqual(len(payload["quests"]), 30)
        self.assertIsInstance(payload["quests"][0]["dialog_accept"], list)


if __name__ == "__main__":
    unittest.main()
