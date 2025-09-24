"""Parser utilities for converting quest documents from plain text."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .models import Quest, QuestDocument

QUEST_HEADER_PATTERN = re.compile(r"^(?P<id>\d+)\.\s*(?P<title>.+)$")


def _normalise_label(label: str) -> str:
    """Convert a label to a simplified ascii identifier."""

    normalised = unicodedata.normalize("NFKD", label).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", normalised).strip().lower()


_FIELD_MAP: Dict[str, Tuple[str, str]] = {
    "mo ta": ("description", "single"),
    "mo ta ": ("description", "single"),
    "description": ("description", "single"),
    "accept npc": ("accept_npc", "single"),
    "accept": ("accept_npc", "single"),
    "complete npc": ("complete_npc", "single"),
    "complete": ("complete_npc", "single"),
    "dialog accept": ("dialog_accept", "list"),
    "dialog accept ": ("dialog_accept", "list"),
    "dialog complete": ("dialog_complete", "list"),
    "dialog finish": ("dialog_complete", "list"),
    "dialog": ("dialog_accept", "list"),
    "target": ("targets", "list"),
    "target 1": ("targets", "list"),
    "target 2": ("targets", "list"),
    "targets": ("targets", "list"),
}

_LIST_FIELDS = {"dialog_accept", "dialog_complete", "targets"}


@dataclass
class _ParseState:
    quest: Quest
    current_field: Optional[str] = None


def _parse_line(state: _ParseState, label: str, value: str) -> None:
    field_info = _FIELD_MAP.get(label)
    if field_info:
        field_name, field_type = field_info
        state.current_field = field_name if field_type == "list" else None

        if field_type == "list":
            entries = [value] if value else []
            getattr(state.quest, field_name).extend(filter(None, [entry.strip() for entry in entries]))
        else:
            if value:
                existing = getattr(state.quest, field_name)
                if existing:
                    merged = f"{existing}\n{value.strip()}"
                else:
                    merged = value.strip()
                setattr(state.quest, field_name, merged)
    else:
        if value:
            state.quest.extra_fields[label] = value.strip()
        state.current_field = None


def _append_to_current(state: _ParseState, line: str) -> None:
    if state.current_field and state.current_field in _LIST_FIELDS:
        getattr(state.quest, state.current_field).append(line.strip())
    else:
        if line.strip():
            state.quest.notes.append(line.strip())


def parse_document(text: str) -> QuestDocument:
    """Parse a quest document from the provided raw text."""

    lines = [line.rstrip() for line in text.splitlines()]

    preamble_lines: List[str] = []
    quests: List[Quest] = []
    current_state: Optional[_ParseState] = None
    in_quests = False
    detail_section_reached = False

    for line in lines:
        stripped = line.strip()
        normalised_line = _normalise_label(stripped) if stripped else ""

        if not detail_section_reached:
            preamble_lines.append(line)
            if normalised_line == "chi tiet":
                detail_section_reached = True
            continue

        if not in_quests:
            header_match = QUEST_HEADER_PATTERN.match(stripped)
            if header_match:
                in_quests = True
            else:
                preamble_lines.append(line)
                continue

        quest_match = QUEST_HEADER_PATTERN.match(stripped)
        if in_quests and quest_match:
            quest_id = int(quest_match.group("id"))
            if current_state is None or quest_id > current_state.quest.id:
                if current_state is not None:
                    quests.append(current_state.quest)
                title = quest_match.group("title").strip()
                current_state = _ParseState(quest=Quest(id=quest_id, title=title))
                continue

        if current_state is None:
            continue

        if not stripped:
            current_state.current_field = None
            continue

        if stripped.startswith("•") or stripped.startswith("-"):
            content = stripped[1:].strip()
            if content.startswith("[") and "]" in content:
                label_part, rest = content.split("]", 1)
                label = label_part[1:].strip()
                value = rest.strip()
                normalised = _normalise_label(label)
                _parse_line(current_state, normalised, value)
            else:
                if content:
                    current_state.quest.notes.append(content)
                current_state.current_field = None
            continue

        if stripped.startswith("o"):
            content = stripped[1:].strip(" \t-•")
            if content:
                _append_to_current(current_state, content)
            continue

        if stripped.startswith("→"):
            current_state.quest.notes.append(stripped)
            continue

        _append_to_current(current_state, stripped)

    if current_state is not None:
        quests.append(current_state.quest)

    title: Optional[str] = None
    overview = ""
    if preamble_lines:
        non_empty = [line for line in preamble_lines if line.strip()]
        if non_empty:
            title = non_empty[0].strip()
        overview = "\n".join(preamble_lines).strip()

    quests.sort(key=lambda q: q.id)

    return QuestDocument(title=title, overview=overview, quests=quests)
