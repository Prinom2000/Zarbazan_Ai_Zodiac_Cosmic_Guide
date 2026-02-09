"""
Numerology Analysis Endpoint
"""

from fastapi import APIRouter, HTTPException

from app.schemas import PersonInput, NumerologyResponse
from app.utils import (
    calculate_life_path,
    calculate_destiny_number,
    calculate_soul_urge
)
from app.services import ai_service

router = APIRouter()


@router.post("/numerology", response_model=NumerologyResponse)
async def numerology_analysis(person: PersonInput):
    """
    Route 4: Numerology Analysis
    Returns: Life path, destiny, soul urge numbers + personality, strengths, challenges, career path
    """
    try:
        # Calculate numerology numbers
        life_path = calculate_life_path(person.birth_date)
        destiny = calculate_destiny_number(person.name)
        soul_urge = calculate_soul_urge(person.name)
        
        # Generate AI insights
        personality_prompt = f"""Provide a personality summary for {person.name} with Life Path {life_path}, 
        Destiny Number {destiny}, and Soul Urge {soul_urge}. 
        Make it personal and insightful. 4-5 sentences."""
        
        strengths_prompt = f"""List the key strengths of someone with Life Path {life_path} and Destiny {destiny}.
        Provide 3-4 specific strengths. Be concise."""
        
        challenges_prompt = f"""List the main challenges for someone with Life Path {life_path} and Soul Urge {soul_urge}.
        Provide 2-3 specific challenges and how to overcome them."""
        
        career_prompt = f"""Suggest ideal career paths for {person.name} with Life Path {life_path} and Destiny {destiny}.
        Include 3-4 specific career suggestions with brief explanations."""
        
        personality_summary = ai_service.generate_content(personality_prompt)
        strengths = ai_service.generate_content(strengths_prompt)
        challenges = ai_service.generate_content(challenges_prompt)
        career_path = ai_service.generate_content(career_prompt)
        
        return {
            "success": True,
            "data": {
                "name": person.name,
                "numerology_numbers": {
                    "life_path": life_path,
                    "destiny_number": destiny,
                    "soul_urge": soul_urge
                },
                "personality_summary": personality_summary,
                "strengths": strengths,
                "challenges": challenges,
                "career_path": career_path
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))