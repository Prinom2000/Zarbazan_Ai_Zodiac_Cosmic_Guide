"""
Pydantic Models for Request/Response Validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class PersonInput(BaseModel):
    user_id: str = Field(..., example="user123")
    name: str = Field(..., example="Prinom Mojumder")
    gender: str = Field(..., example="Male")
    birth_date: str = Field(..., example="2000-04-11")
    birth_time: str = Field(..., example="13:00")
    birth_place: str = Field(..., example="Dhaka")


class TwoPersonInput(BaseModel):
    user_id: str = Field(..., example="user123")
    person1: PersonInput
    person2: PersonInput


class TarotInput(BaseModel):
    user_id: str = Field(..., example="user123")
    cards: List[str] = Field(..., example=["The Fool", "The Magician", "The Lovers"])


# Response Models
class SunPositionResponse(BaseModel):
    sign: str
    degree: float


class MoonPositionResponse(BaseModel):
    sign: str
    degree: float


class DailyHoroscopeResponse(BaseModel):
    success: bool
    data: Dict


class ExtendedHoroscopeResponse(BaseModel):
    success: bool
    data: Dict


class CompatibilityResponse(BaseModel):
    success: bool
    data: Dict


class NumerologyResponse(BaseModel):
    success: bool
    data: Dict


class CompleteAnalysisResponse(BaseModel):
    success: bool
    data: Dict


class TarotReadingResponse(BaseModel):
    success: bool
    data: Dict