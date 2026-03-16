"""
Compatibility Analysis Endpoint (Kundali Matching)
"""

from fastapi import APIRouter, HTTPException
import swisseph as swe

from app.schemas import TwoPersonInput, CompatibilityResponse
from app.utils import (
    parse_birth_datetime,
    get_location_data,
    get_julian_day,
    get_planet_position,
    get_moon_nakshatra,
    calculate_compatibility_scores
)
from app.data.nakshatra_data import nakshatras
from app.services import ai_service

router = APIRouter()


@router.post("/compatibility", response_model=CompatibilityResponse)
async def compatibility_analysis(data: TwoPersonInput):
    """
    Route 3: Compatibility Analysis (Kundali Matching)
    Returns: Compatibility scores, emotional bond, communication, growth areas
    """
    try:
        # Person 1 data
        birth_dt1 = parse_birth_datetime(data.person1.birth_date, data.person1.birth_time)
        location1 = get_location_data(data.person1.birth_place)
        jd1 = get_julian_day(
            birth_dt1.year, birth_dt1.month, birth_dt1.day,
            birth_dt1.hour, birth_dt1.minute, location1["tz"]
        )
        moon_lon1 = get_planet_position(jd1, swe.MOON, use_sidereal=True)
        nak_idx1 = get_moon_nakshatra(moon_lon1)
        
        # Person 2 data
        birth_dt2 = parse_birth_datetime(data.person2.birth_date, data.person2.birth_time)
        location2 = get_location_data(data.person2.birth_place)
        jd2 = get_julian_day(
            birth_dt2.year, birth_dt2.month, birth_dt2.day,
            birth_dt2.hour, birth_dt2.minute, location2["tz"]
        )
        moon_lon2 = get_planet_position(jd2, swe.MOON, use_sidereal=True)
        nak_idx2 = get_moon_nakshatra(moon_lon2)
        
        # Calculate compatibility scores
        scores = calculate_compatibility_scores(nak_idx1, nak_idx2)
        
        # Generate AI insights
        emotional_prompt = f"""Analyze the emotional bond between {data.person1.name} and {data.person2.name}.
        Their compatibility scores are: Love {scores['Love']}%, Trust {scores['Trust']}%.
        Provide insights on their emotional connection. 3-4 sentences."""
        
        communication_prompt = f"""Analyze the communication dynamics between {data.person1.name} and {data.person2.name}.
        Their compatibility scores show Trust {scores['Trust']}%, Lifestyle {scores['Lifestyle']}%.
        Provide insights on how they communicate. 3-4 sentences."""
        
        growth_prompt = f"""Identify growth areas for the relationship between {data.person1.name} and {data.person2.name}.
        Their scores: Family {scores['Family']}%, Longevity {scores['Longevity']}%, Overall {scores['Overall']}%.
        Provide 3 specific areas where they can grow together. 3-4 sentences."""
        
        emotional_bond = ai_service.generate_content(emotional_prompt)
        communication = ai_service.generate_content(communication_prompt)
        growth_areas = ai_service.generate_content(growth_prompt)
        
        return {
            "success": True,
            "data": {
                "user_id": data.person1.user_id,
                "person1": {
                    "name": data.person1.name,
                    "nakshatra": nakshatras[nak_idx1]
                },
                "person2": {
                    "name": data.person2.name,
                    "nakshatra": nakshatras[nak_idx2]
                },
                "compatibility_scores": scores,
                "emotional_bond": emotional_bond,
                "communication": communication,
                "growth_areas": growth_areas
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))