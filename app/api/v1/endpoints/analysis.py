"""
Complete Life Analysis Endpoint
"""

from fastapi import APIRouter, HTTPException
import swisseph as swe
import datetime

from app.schemas import PersonInput, CompleteAnalysisResponse
from app.utils import (
    parse_birth_datetime,
    get_location_data,
    get_julian_day,
    get_planet_position,
    get_zodiac_sign,
    calculate_life_path,
    calculate_destiny_number
)
from app.services import ai_service

router = APIRouter()


@router.post("/complete-analysis", response_model=CompleteAnalysisResponse)
async def complete_life_analysis(person: PersonInput):
    """
    Route 5: Complete Life Analysis
    Returns: Deep analysis, lucky elements, 3-year forecast
    """
    try:
        # Calculate astrology data
        birth_dt = parse_birth_datetime(person.birth_date, person.birth_time)
        location = get_location_data(person.birth_place)
        jd = get_julian_day(
            birth_dt.year, birth_dt.month, birth_dt.day,
            birth_dt.hour, birth_dt.minute, location["tz"]
        )
        
        sun_lon = get_planet_position(jd, swe.SUN, use_sidereal=False)
        moon_lon = get_planet_position(jd, swe.MOON, use_sidereal=False)
        sun_sign = get_zodiac_sign(sun_lon)
        moon_sign = get_zodiac_sign(moon_lon)
        
        # Calculate numerology
        life_path = calculate_life_path(person.birth_date)
        destiny = calculate_destiny_number(person.name)
        
        # Generate comprehensive AI insights
        personality_prompt = f"""Provide a deep personality analysis for {person.name}, a {sun_sign} sun with {moon_sign} moon,
        Life Path {life_path}. Explore their core nature, motivations, and unique traits. 5-6 sentences."""
        
        life_destiny_prompt = f"""Analyze the life path and destiny for {person.name} with Life Path {life_path} and Destiny {destiny}.
        What is their soul's purpose? 4-5 sentences."""
        
        career_business_prompt = f"""Provide career and business guidance for {person.name} ({sun_sign} with Life Path {life_path}).
        Include entrepreneurial potential and professional strengths. 4-5 sentences."""
        
        love_relationship_prompt = f"""Analyze love and relationship patterns for {person.name} ({sun_sign} sun, {moon_sign} moon).
        Include compatibility needs and relationship advice. 4-5 sentences."""
        
        wealth_finance_prompt = f"""Provide wealth and finance guidance for {person.name} with Life Path {life_path} and {sun_sign} sun.
        Include money mindset and financial opportunities. 3-4 sentences."""
        
        health_wellness_prompt = f"""Provide health and wellness insights for {person.name} as a {sun_sign} with {moon_sign} moon.
        Include physical and mental health focus areas. 3-4 sentences."""
        
        # Lucky elements based on sun sign and life path
        lucky_colors = {
            "Aries": ["Red", "Orange"], "Taurus": ["Green", "Pink"], "Gemini": ["Yellow", "Light Blue"],
            "Cancer": ["Silver", "White"], "Leo": ["Gold", "Orange"], "Virgo": ["Navy", "Grey"],
            "Libra": ["Pink", "Light Blue"], "Scorpio": ["Maroon", "Black"], "Sagittarius": ["Purple", "Blue"],
            "Capricorn": ["Brown", "Black"], "Aquarius": ["Blue", "Silver"], "Pisces": ["Sea Green", "Lavender"]
        }
        
        gemstones = {
            "Aries": ["Diamond", "Bloodstone"], "Taurus": ["Emerald", "Rose Quartz"], "Gemini": ["Agate", "Citrine"],
            "Cancer": ["Pearl", "Moonstone"], "Leo": ["Ruby", "Amber"], "Virgo": ["Peridot", "Sapphire"],
            "Libra": ["Opal", "Lapis Lazuli"], "Scorpio": ["Topaz", "Obsidian"], "Sagittarius": ["Turquoise", "Amethyst"],
            "Capricorn": ["Garnet", "Onyx"], "Aquarius": ["Aquamarine", "Amethyst"], "Pisces": ["Aquamarine", "Jade"]
        }
        
        directions = {
            "Aries": "East", "Taurus": "Southeast", "Gemini": "West",
            "Cancer": "North", "Leo": "East", "Virgo": "South",
            "Libra": "West", "Scorpio": "North", "Sagittarius": "Northeast",
            "Capricorn": "South", "Aquarius": "Southwest", "Pisces": "North"
        }
        
        # Generate forecasts for 3 years
        current_year = datetime.datetime.now().year
        forecast_prompt = f"""Provide a year forecast for {person.name} ({sun_sign}, Life Path {life_path}) for the year {{year}}.
        Include key themes, opportunities, and advice. 3-4 sentences."""
        
        forecast_2025 = ai_service.generate_content(forecast_prompt.format(year=current_year), max_tokens=400)
        forecast_2026 = ai_service.generate_content(forecast_prompt.format(year=current_year + 1), max_tokens=400)
        forecast_2027 = ai_service.generate_content(forecast_prompt.format(year=current_year + 2), max_tokens=400)
        
        return {
            "success": True,
            "data": {
                "name": person.name,
                "astrological_profile": {
                    "sun_sign": sun_sign,
                    "moon_sign": moon_sign,
                    "life_path": life_path
                },
                "deep_analysis": {
                    "personality_analysis": ai_service.generate_content(personality_prompt, max_tokens=600),
                    "life_path_destiny": ai_service.generate_content(life_destiny_prompt, max_tokens=500),
                    "career_business": ai_service.generate_content(career_business_prompt, max_tokens=500),
                    "love_relationship": ai_service.generate_content(love_relationship_prompt, max_tokens=500),
                    "wealth_finance": ai_service.generate_content(wealth_finance_prompt, max_tokens=400),
                    "health_wellness": ai_service.generate_content(health_wellness_prompt, max_tokens=400)
                },
                "lucky_elements": {
                    "lucky_number": life_path,
                    "power_colors": lucky_colors.get(sun_sign, ["Blue", "White"]),
                    "gemstones": gemstones.get(sun_sign, ["Clear Quartz"]),
                    "best_direction": directions.get(sun_sign, "North")
                },
                "future_forecast": [
                    {"year": current_year, "forecast": forecast_2025},
                    {"year": current_year + 1, "forecast": forecast_2026},
                    {"year": current_year + 2, "forecast": forecast_2027}
                ]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))