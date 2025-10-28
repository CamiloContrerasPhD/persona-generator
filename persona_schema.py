from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class Psychographics(BaseModel):
    values: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    lifestyle: List[str] = Field(default_factory=list)


class Persona(BaseModel):
    name: str
    age_range: str
    gender: Optional[str] = None
    location: Optional[str] = None
    occupation: Optional[str] = None
    income_range: Optional[str] = None
    education: Optional[str] = None
    motivations: List[str] = Field(default_factory=list)
    frustrations: List[str] = Field(default_factory=list)
    preferred_channels: List[str] = Field(default_factory=list)
    messaging_tone: Optional[str] = None
    psychographics: Psychographics = Field(default_factory=Psychographics)
    summary: Optional[str] = None
    # Conductual/behavioral segmentation signals
    behavioral_signals: List[str] = Field(default_factory=list)
    # Multi-level segmentation: e.g., Macro > Micro > Niche
    segmentation_levels: List[dict] = Field(default_factory=list)
    # Narrative brief for message recipients (channels + key message, CTA, rationale)
    creative_brief: Optional[str] = None
    # Value canvas-like structure
    value_canvas: Optional[dict] = None
    # Empathy map-like structure
    empathy_map: Optional[dict] = None


class PersonaBundle(BaseModel):
    personas: List[Persona] = Field(default_factory=list)

