"""
Horoscope Endpoints (Daily & Extended)
"""

from fastapi import APIRouter, HTTPException
import swisseph as swe
import datetime

from app.schemas import (
    PersonInput,
    DailyHoroscopeResponse,
    ExtendedHoroscopeResponse
)
from app.utils import (
    parse_birth_datetime,
    get_location_data,
    get_julian_day,
    get_planet_position,
    get_zodiac_sign
)
from app.services import ai_service

router = APIRouter()


@router.post("/daily-horoscope", response_model=DailyHoroscopeResponse)
async def daily_horoscope(person: PersonInput):
    """
    Route 1: Daily Horoscope
    Returns: Zodiac sign, Sun/Moon positions, daily horoscope, career/finance, health/energy insights
    """
    try:
        # Parse birth data
        birth_dt = parse_birth_datetime(person.birth_date, person.birth_time)
        location = get_location_data(person.birth_place)
        
        # Calculate Julian Day
        jd = get_julian_day(
            birth_dt.year, birth_dt.month, birth_dt.day,
            birth_dt.hour, birth_dt.minute, location["tz"]
        )
        
        # Get Sun and Moon positions (tropical for Western zodiac)
        sun_lon = get_planet_position(jd, swe.SUN, use_sidereal=False)
        moon_lon = get_planet_position(jd, swe.MOON, use_sidereal=False)
        
        # Get zodiac signs
        sun_sign = get_zodiac_sign(sun_lon)
        moon_sign = get_zodiac_sign(moon_lon)
        
        # Generate AI content
        today = datetime.datetime.now().strftime("%B %d, %Y")
        
        horoscope_prompt = f"""Generate a personalized daily horoscope for {person.name}, a {sun_sign} sun sign and {moon_sign} moon sign, for today ({today}). 
        Write it in second person ('you'), make it inspiring and specific. Include cosmic influences. Keep it 3-4 sentences."""
        
        career_prompt = f"""Provide daily career and finance insights for a {sun_sign} person named {person.name} for today.
        Include specific actionable advice. Keep it 2-3 sentences."""
        
        health_prompt = f"""Provide daily health and energy insights for a {sun_sign} with {moon_sign} moon for today.
        Include wellness tips and energy forecast. Keep it 2-3 sentences."""
        
        daily_horoscope_text = ai_service.generate_content(horoscope_prompt)
        career_finance = ai_service.generate_content(career_prompt)
        health_energy = ai_service.generate_content(health_prompt)
        
        return {
            "success": True,
            "data": {
                "user_id": person.user_id,
                "name": person.name,
                "zodiac_sign": sun_sign,
                "sun_position": {
                    "sign": sun_sign,
                    "degree": round(sun_lon % 30, 2)
                },
                "moon_position": {
                    "sign": moon_sign,
                    "degree": round(moon_lon % 30, 2)
                },
                "today_horoscope": daily_horoscope_text,
                "career_finance_insights": career_finance,
                "health_energy_insights": health_energy,
                "date": today
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extended-horoscope", response_model=ExtendedHoroscopeResponse)
async def extended_horoscope(person: PersonInput):
    """
    Route 2: Weekly & Monthly Horoscope
    Returns: Weekly forecast, monthly forecast, love insights, opportunities, challenges, important dates
    """
    try:
        # Parse birth data
        birth_dt = parse_birth_datetime(person.birth_date, person.birth_time)
        location = get_location_data(person.birth_place)
        
        jd = get_julian_day(
            birth_dt.year, birth_dt.month, birth_dt.day,
            birth_dt.hour, birth_dt.minute, location["tz"]
        )
        
        sun_lon = get_planet_position(jd, swe.SUN, use_sidereal=False)
        sun_sign = get_zodiac_sign(sun_lon)
        
        # Current date info
        now = datetime.datetime.now()
        current_month = now.strftime("%B %Y")
        
        # Generate AI content
        weekly_prompt = f"""Generate a weekly horoscope for {person.name}, a {sun_sign}, for the upcoming week.
        Cover key themes, opportunities, and advice. Make it personal and specific. 4-5 sentences."""
        
        monthly_prompt = f"""Generate a monthly horoscope for {person.name}, a {sun_sign}, for {current_month}.
        Cover major themes, planetary influences, and what to expect. 5-6 sentences."""
        
        love_prompt = f"""Provide love and relationship insights for a {sun_sign} named {person.name} for this week.
        Include romantic forecast and relationship advice. 3-4 sentences."""
        
        opportunity_prompt = f"""Identify the key opportunity for {person.name} ({sun_sign}) this month in {current_month}.
        Be specific and actionable. 2-3 sentences."""
        
        challenge_prompt = f"""Identify the main challenge for {person.name} ({sun_sign}) this month in {current_month}.
        Include how to overcome it. 2-3 sentences."""
        
        dates_prompt = f"""List 3 important dates in {current_month} for a {sun_sign} person. 
        For each date, provide: the date (format: Month DD), and a brief reason (one sentence).
        Format as: 1. [Date] - [Reason]"""
        
        weekly_horoscope = ai_service.generate_content(weekly_prompt)
        monthly_horoscope = ai_service.generate_content(monthly_prompt)
        love_insights = ai_service.generate_content(love_prompt)
        key_opportunity = ai_service.generate_content(opportunity_prompt)
        challenge = ai_service.generate_content(challenge_prompt)
        important_dates_text = ai_service.generate_content(dates_prompt, max_tokens=300)
        
        return {
            "success": True,
            "data": {
                "user_id": person.user_id,
                "name": person.name,
                "zodiac_sign": sun_sign,
                "weekly_horoscope": weekly_horoscope,
                "monthly_horoscope": monthly_horoscope,
                "love_relationship_insights": love_insights,
                "key_opportunity_this_month": key_opportunity,
                "challenge_this_month": challenge,
                "important_dates": important_dates_text,
                "month": current_month
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))