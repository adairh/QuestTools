"""Utility helpers for storing and loading quest documents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .models import Quest, QuestDocument


def _quest_from_dict(data: Dict[str, object]) -> Quest:
    """Create a :class:`Quest` instance from a dictionary."""

    return Quest(
        id=int(data.get("id", 0)),
        title=str(data.get("title", "")),
        description=data.get("description"),
        accept_npc=data.get("accept_npc"),
        complete_npc=data.get("complete_npc"),
        dialog_accept=list(data.get("dialog_accept", []) or []),
        dialog_complete=list(data.get("dialog_complete", []) or []),
        targets=list(data.get("targets", []) or []),
        notes=list(data.get("notes", []) or []),
        extra_fields=dict(data.get("extra_fields", {}) or {}),
    )


def load_document(path: Path | str) -> QuestDocument:
    """Load a quest document from a JSON file."""

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Quest data file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    quests_data: List[Dict[str, object]] = data.get("quests", [])
    quests = [_quest_from_dict(item) for item in quests_data]

    return QuestDocument(
        title=data.get("title"),
        overview=str(data.get("overview", "")),
        quests=quests,
    )


def save_document(path: Path | str, document: QuestDocument) -> None:
    """Serialise a quest document to a JSON file."""

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    payload = document.to_dict()

    with file_path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
