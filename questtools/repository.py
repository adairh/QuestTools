"""High-level repository for quest data persistence."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Iterable, Optional

from .models import Quest, QuestDocument
from .storage import load_document, save_document


class QuestRepository:
    """Provide thread-safe access to quest documents."""

    _QUEST_FIELDS = {
        "title",
        "description",
        "accept_npc",
        "complete_npc",
        "dialog_accept",
        "dialog_complete",
        "targets",
        "notes",
        "extra_fields",
    }

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._lock = Lock()
        self._document: Optional[QuestDocument] = None

    def _ensure_document(self) -> QuestDocument:
        if self._document is None:
            if self.path.exists():
                self._document = load_document(self.path)
            else:
                self._document = QuestDocument(title=None, overview="", quests=[])
        return self._document

    def _persist(self) -> None:
        document = self._ensure_document()
        save_document(self.path, document)

    def _clone(self, document: QuestDocument) -> QuestDocument:
        return deepcopy(document)

    def _clone_quest(self, quest: Quest) -> Quest:
        return deepcopy(quest)

    def get_document(self) -> QuestDocument:
        with self._lock:
            document = self._ensure_document()
            return self._clone(document)

    def list_quests(self) -> Iterable[Quest]:
        document = self.get_document()
        return document.quests

    def _find_quest(self, document: QuestDocument, quest_id: int) -> Quest:
        for quest in document.quests:
            if quest.id == quest_id:
                return quest
        raise KeyError(f"Quest with id {quest_id} not found")

    def get_quest(self, quest_id: int) -> Quest:
        with self._lock:
            document = self._ensure_document()
            quest = self._find_quest(document, quest_id)
            return self._clone_quest(quest)

    def _next_id(self, document: QuestDocument) -> int:
        if not document.quests:
            return 1
        return max(quest.id for quest in document.quests) + 1

    def create_quest(self, data: Dict[str, Any]) -> Quest:
        if not data.get("title"):
            raise ValueError("Quest title is required")

        with self._lock:
            document = self._ensure_document()
            quest = Quest(id=self._next_id(document), title=str(data["title"]))

            for field in self._QUEST_FIELDS - {"title"}:
                if field in data and data[field] is not None:
                    setattr(quest, field, self._normalise_field(field, data[field]))

            document.quests.append(quest)
            self._persist()
            return self._clone_quest(quest)

    def update_quest(self, quest_id: int, data: Dict[str, Any]) -> Quest:
        with self._lock:
            document = self._ensure_document()
            quest = self._find_quest(document, quest_id)

            if "title" in data and data["title"] is not None:
                quest.title = str(data["title"])

            for field in self._QUEST_FIELDS - {"title"}:
                if field in data:
                    value = data[field]
                    if value is None:
                        if isinstance(getattr(quest, field), list):
                            setattr(quest, field, [])
                        else:
                            setattr(quest, field, None)
                    else:
                        setattr(quest, field, self._normalise_field(field, value))

            self._persist()
            return self._clone_quest(quest)

    def delete_quest(self, quest_id: int) -> None:
        with self._lock:
            document = self._ensure_document()
            original_length = len(document.quests)
            document.quests = [quest for quest in document.quests if quest.id != quest_id]
            if len(document.quests) == original_length:
                raise KeyError(f"Quest with id {quest_id} not found")
            self._persist()

    def update_document(self, *, title: Optional[str], overview: str) -> QuestDocument:
        with self._lock:
            document = self._ensure_document()
            document.title = title
            document.overview = overview
            self._persist()
            return self._clone(document)

    def _normalise_field(self, field: str, value: Any) -> Any:
        if field in {"dialog_accept", "dialog_complete", "targets", "notes"}:
            if isinstance(value, str):
                return [item for item in value.splitlines() if item.strip()]
            if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
                return [str(item) for item in value]
            raise TypeError(f"Invalid value for {field}: {value!r}")
        if field == "extra_fields":
            if not isinstance(value, dict):
                raise TypeError("extra_fields must be a mapping")
            return {str(k): str(v) for k, v in value.items()}
        return value
