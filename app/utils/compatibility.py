"""
Compatibility Utility Functions (Kundali Matching)
"""

from app.data.nakshatra_data import (
    nakshatra_lords,
    nakshatra_gana,
    nakshatra_nadi,
    nakshatra_yoni
)


def are_planets_friends(planet1: str, planet2: str) -> int:
    """Check planetary friendship"""
    if planet1 == planet2:
        return 2
    
    friendship = {
        "Sun": {"friends": ["Moon", "Mars", "Jupiter"], "neutral": ["Mercury"], "enemy": ["Venus", "Saturn"]},
        "Moon": {"friends": ["Sun", "Mercury"], "neutral": ["Mars", "Jupiter", "Venus", "Saturn"], "enemy": []},
        "Mars": {"friends": ["Sun", "Moon", "Jupiter"], "neutral": ["Venus", "Saturn"], "enemy": ["Mercury"]},
        "Mercury": {"friends": ["Sun", "Venus"], "neutral": ["Mars", "Jupiter", "Saturn"], "enemy": ["Moon"]},
        "Jupiter": {"friends": ["Sun", "Moon", "Mars"], "neutral": ["Saturn"], "enemy": ["Mercury", "Venus"]},
        "Venus": {"friends": ["Mercury", "Saturn"], "neutral": ["Mars", "Jupiter"], "enemy": ["Sun", "Moon"]},
        "Saturn": {"friends": ["Mercury", "Venus"], "neutral": ["Jupiter"], "enemy": ["Sun", "Moon", "Mars"]},
        "Rahu": {"friends": ["Venus", "Saturn"], "neutral": ["Mercury"], "enemy": ["Sun", "Moon", "Mars"]},
        "Ketu": {"friends": ["Mars", "Jupiter"], "neutral": ["Venus", "Saturn"], "enemy": ["Sun", "Moon"]}
    }
    
    if planet2 in friendship.get(planet1, {}).get("friends", []):
        return 2
    elif planet2 in friendship.get(planet1, {}).get("neutral", []):
        return 1
    else:
        return 0


def calculate_compatibility_scores(nak_idx1: int, nak_idx2: int) -> dict:
    """Calculate Vedic compatibility scores"""
    lord1 = nakshatra_lords[nak_idx1]
    lord2 = nakshatra_lords[nak_idx2]
    gana1 = nakshatra_gana[nak_idx1]
    gana2 = nakshatra_gana[nak_idx2]
    nadi1 = nakshatra_nadi[nak_idx1]
    nadi2 = nakshatra_nadi[nak_idx2]
    yoni1 = nakshatra_yoni[nak_idx1]
    yoni2 = nakshatra_yoni[nak_idx2]
    
    graha_maitri = are_planets_friends(lord1, lord2)
    
    if gana1 == gana2:
        gana_score = 6
    elif abs(gana1 - gana2) == 1:
        gana_score = 3
    else:
        gana_score = 1
    
    yoni_diff = abs(yoni1 - yoni2)
    if yoni_diff == 0:
        yoni_score = 4
    elif yoni_diff <= 2:
        yoni_score = 3
    elif yoni_diff <= 4:
        yoni_score = 2
    else:
        yoni_score = 1
    
    nadi_score = 8 if nadi1 != nadi2 else 0
    
    tara_count = (nak_idx2 - nak_idx1) % 27
    favorable_taras = [0, 2, 4, 6, 8, 10, 12, 15, 17, 19, 24, 26]
    tara_score = 3 if tara_count in favorable_taras else 1
    
    nak_diff = abs(nak_idx1 - nak_idx2)
    vashya_score = 2 if (nak_diff <= 3 or nak_diff >= 24) else 1
    
    rashi1 = nak_idx1 // 2.25
    rashi2 = nak_idx2 // 2.25
    rashi_diff = abs(rashi1 - rashi2) % 12
    bhakoot_score = 7 if rashi_diff in [2, 3, 4, 5, 9, 10, 11] else 2
    
    love_raw = (graha_maitri * 2.5 + gana_score * 1.5 + yoni_score * 2.5 + vashya_score * 5) / 20
    trust_raw = (graha_maitri * 2.5 + tara_score * 2.5) / 10
    family_raw = (nadi_score + bhakoot_score + gana_score) / 21
    longevity_raw = (nadi_score + yoni_score * 2 + tara_score * 2) / 15
    lifestyle_raw = (gana_score * 1.5 + graha_maitri * 2) / 11
    
    love = int(love_raw * 100)
    trust = int(trust_raw * 100)
    family = int(family_raw * 100)
    longevity = int(longevity_raw * 100)
    lifestyle = int(lifestyle_raw * 100)
    overall = int((love + trust + family + longevity + lifestyle) / 5)
    
    return {
        "Love": min(100, max(0, love)),
        "Trust": min(100, max(0, trust)),
        "Family": min(100, max(0, family)),
        "Longevity": min(100, max(0, longevity)),
        "Lifestyle": min(100, max(0, lifestyle)),
        "Overall": min(100, max(0, overall))
    }