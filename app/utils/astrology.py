"""
Astrology Utility Functions
"""

import swisseph as swe
import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz


def get_location_data(location_string: str) -> dict:
    """Get latitude, longitude, and timezone offset for any location"""
    try:
        geolocator = Nominatim(user_agent="astrology_api")
        location = geolocator.geocode(location_string)
        
        if location is None:
            return {"lat": 23.8103, "lon": 90.4125, "tz": 6.0}
        
        lat = location.latitude
        lon = location.longitude
        
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lat=lat, lng=lon)
        
        if tz_name is None:
            tz_offset = 6.0
        else:
            tz = pytz.timezone(tz_name)
            offset = tz.utcoffset(datetime.datetime(2024, 1, 1))
            tz_offset = offset.total_seconds() / 3600
        
        return {"lat": lat, "lon": lon, "tz": tz_offset}
    
    except Exception as e:
        print(f"Error geocoding: {e}")
        return {"lat": 23.8103, "lon": 90.4125, "tz": 6.0}


def parse_birth_datetime(date_str: str, time_str: str) -> datetime.datetime:
    """Parse birth date and time strings into datetime object"""
    date_parts = date_str.split("-")
    time_parts = time_str.split(":")
    
    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])
    hour = int(time_parts[0])
    minute = int(time_parts[1]) if len(time_parts) > 1 else 0
    
    return datetime.datetime(year, month, day, hour, minute)


def get_julian_day(year: int, month: int, day: int, hour: int, minute: int, tz_offset: float) -> float:
    """Convert local time to Julian Day"""
    utc_hour = hour - tz_offset
    return swe.julday(year, month, day, utc_hour + minute / 60.0)


def get_planet_position(jd: float, planet: int, use_sidereal: bool = True) -> float:
    """Get planet's longitude"""
    if use_sidereal:
        swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    result = swe.calc_ut(jd, planet, swe.FLG_SWIEPH | (swe.FLG_SIDEREAL if use_sidereal else 0))
    
    def find_number(x):
        if isinstance(x, (int, float)):
            return x
        if isinstance(x, (tuple, list)) and x:
            for item in x:
                num = find_number(item)
                if num is not None:
                    return num
        return None
    
    lon = find_number(result)
    if lon is None:
        raise RuntimeError(f"Cannot extract longitude from: {result}")
    
    lon = lon % 360
    if lon < 0:
        lon += 360
    
    return lon


def get_zodiac_sign(longitude: float) -> str:
    """Get zodiac sign from tropical longitude"""
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    index = int(longitude / 30)
    return signs[index % 12]


def get_moon_nakshatra(lon: float) -> int:
    """Get nakshatra index from sidereal longitude"""
    nakshatra_span = 360.0 / 27.0
    index = int(lon / nakshatra_span)
    return max(0, min(26, index))