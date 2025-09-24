"""Data models for representing quest documents."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional


@dataclass
class Quest:
    """Represent a single quest entry."""

    id: int
    title: str
    description: Optional[str] = None
    accept_npc: Optional[str] = None
    complete_npc: Optional[str] = None
    dialog_accept: List[str] = field(default_factory=list)
    dialog_complete: List[str] = field(default_factory=list)
    targets: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    extra_fields: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        """Convert the quest to a serialisable dictionary."""

        return asdict(self)


@dataclass
class QuestDocument:
    """Representation of an entire quest document."""

    title: Optional[str]
    overview: str
    quests: List[Quest] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        """Convert the document to a serialisable dictionary."""

        return {
            "title": self.title,
            "overview": self.overview,
            "quests": [quest.to_dict() for quest in self.quests],
        }
