"""Pydantic schemas for the QuestTools web API."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class QuestBase(BaseModel):
    description: Optional[str] = None
    accept_npc: Optional[str] = None
    complete_npc: Optional[str] = None
    dialog_accept: List[str] = Field(default_factory=list)
    dialog_complete: List[str] = Field(default_factory=list)
    targets: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    extra_fields: Dict[str, str] = Field(default_factory=dict)


class QuestCreate(QuestBase):
    title: str


class QuestUpdate(QuestBase):
    title: Optional[str] = None


class QuestResponse(QuestBase):
    id: int
    title: str


class DocumentResponse(BaseModel):
    title: Optional[str]
    overview: str
    quests: List[QuestResponse]


class DocumentUpdate(BaseModel):
    title: Optional[str]
    overview: str
