"""
Video Generation Endpoints
"""

import os
import time
import requests
import datetime
from fastapi import APIRouter, HTTPException
from app.schemas import PersonInput, TarotInput, TwoPersonInput
import openai

router = APIRouter()

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

# OpenAI client
openai.api_key = OPENAI_API_KEY


@router.post("/horoscope-video")
async def horoscope_video(person: PersonInput):
    """
    Generate a horoscope video for the user.
    Takes person details, generates horoscope summary using OpenAI,
    creates video with HeyGen, uploads to Cloudinary, and returns text & video link.
    """
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Generate horoscope summary using OpenAI
        prompt = f"""Generate a personalized daily horoscope summary for {person.name}, born on {person.birth_date} at {person.birth_time} in {person.birth_place}.

        Rules:
        - Write 2-3 complete sentences only.
        - Every sentence must end with a period.
        - Total length must be between 280-320 characters including spaces.
        - Do NOT cut off mid-sentence.
        - Count characters carefully before responding."""

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,  # 320 chars ≈ ~80 tokens, 150 gives safe buffer
            temperature=0.7
        )

        
        summary_text = response.choices[0].message.content.strip()
        
        # # Ensure the text is within character limits (optional adjustment)
        # char_count = len(summary_text)
        # if char_count < 280:
        #     # If too short, we can regenerate or accept, but for now proceed
        #     pass
        # elif char_count > 320:
        #     summary_text = summary_text[:320]  # Truncate if too long
        
        # HeyGen API setup
        BASE_URL = "https://api.heygen.com"
        HEADERS = {
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Create video payload
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": "Anna_public_3_20240108",  # Default avatar
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": summary_text,
                        "voice_id": "2d5b0e6cf36f460aa7fc47e3eee4ba54",  # Default voice
                        "speed": 1.0
                    },
                    "background": {
                        "type": "color",
                        "value": "#ffffff"  # White background
                    }
                }
            ],
            "dimension": {
                "width": 1280,
                "height": 720
            }
        }
        
        # Submit video generation request
        response = requests.post(f"{BASE_URL}/v2/video/generate", headers=HEADERS, json=payload)
        response.raise_for_status()
        
        video_id = response.json()["data"]["video_id"]
        
        # Wait for video to be ready
        def wait_for_video(vid):
            url = f"{BASE_URL}/v1/video_status.get?video_id={vid}"
            elapsed = 0
            timeout = 300  # 5 minutes
            while elapsed < timeout:
                resp = requests.get(url, headers=HEADERS)
                resp.raise_for_status()
                data = resp.json()["data"]
                status = data.get("status")
                if status == "completed":
                    return data["video_url"]
                elif status == "failed":
                    error = data.get("error", "Unknown error")
                    raise RuntimeError(f"Video generation failed: {error}")
                time.sleep(5)
                elapsed += 5
            raise TimeoutError("Timed out waiting for video generation.")
        
        video_url = wait_for_video(video_id)
        
        return {
            "success": True,
            "user_id": person.user_id,
            "date": current_date,
            "data": {
                "horoscope_text": summary_text,
                "video_link": video_url
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/numerology-video")
async def numerology_video(person: PersonInput):
    """
    Generate a numerology video for the user.
    Takes person details, generates numerology summary using OpenAI,
    creates video with HeyGen, and returns text & video link.
    """
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Generate numerology summary using OpenAI
        prompt = f"""Generate a personalized numerology summary for {person.name}, born on {person.birth_date}.

        Rules:
        - Include life path number, destiny number, and key insights.
        - Write 3-4 complete sentences only.
        - Every sentence must end with a period.
        - Total length must be between 450-500 characters including spaces.
        - Do NOT cut off mid-sentence.
        - Count characters carefully before responding."""

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,  # 500 chars ≈ ~125 tokens, 250 gives safe buffer
            temperature=0.7
        )
        
        summary_text = response.choices[0].message.content.strip()
        
        # Ensure the text is within character limits
        # char_count = len(summary_text)
        # if char_count < 450:
        #     pass
        # elif char_count > 500:
        #     summary_text = summary_text[:500]
        
        # HeyGen API setup
        BASE_URL = "https://api.heygen.com"
        HEADERS = {
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Create video payload
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": "Anna_public_3_20240108",
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": summary_text,
                        "voice_id": "2d5b0e6cf36f460aa7fc47e3eee4ba54",
                        "speed": 1.0
                    },
                    "background": {
                        "type": "color",
                        "value": "#ffffff"
                    }
                }
            ],
            "dimension": {
                "width": 1280,
                "height": 720
            }
        }
        
        # Submit video generation request
        response = requests.post(f"{BASE_URL}/v2/video/generate", headers=HEADERS, json=payload)
        response.raise_for_status()
        
        video_id = response.json()["data"]["video_id"]
        
        # Wait for video to be ready
        def wait_for_video(vid):
            url = f"{BASE_URL}/v1/video_status.get?video_id={vid}"
            elapsed = 0
            timeout = 300
            while elapsed < timeout:
                resp = requests.get(url, headers=HEADERS)
                resp.raise_for_status()
                data = resp.json()["data"]
                status = data.get("status")
                if status == "completed":
                    return data["video_url"]
                elif status == "failed":
                    error = data.get("error", "Unknown error")
                    raise RuntimeError(f"Video generation failed: {error}")
                time.sleep(5)
                elapsed += 5
            raise TimeoutError("Timed out waiting for video generation.")
        
        video_url = wait_for_video(video_id)
        
        return {
            "success": True,
            "user_id": person.user_id,
            "date": current_date,
            "data": {
                "numerology_text": summary_text,
                "video_link": video_url
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tarot-video")
async def tarot_video(data: TarotInput):
    """
    Generate a tarot video for the user.
    Takes tarot cards, generates reading using OpenAI,
    creates video with HeyGen, and returns text & video link.
    """
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        cards_str = ", ".join(data.cards)
        # Generate tarot reading using OpenAI
        prompt = f"""Generate a detailed tarot reading for the cards: {cards_str}.

        Rules:
        - Cover past, present, future, and advice — one sentence each.
        - Write exactly 4 complete sentences.
        - Every sentence must end with a period.
        - Total length must be between 650-750 characters including spaces.
        - Do NOT cut off mid-sentence.
        - Count characters carefully before responding."""

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,  # 750 chars ≈ ~190 tokens, 300 gives safe buffer
            temperature=0.7
        )
        
        summary_text = response.choices[0].message.content.strip()
        
        # Ensure the text is within character limits
        # char_count = len(summary_text)
        # if char_count < 650:
        #     pass
        # elif char_count > 750:
        #     summary_text = summary_text[:750]
        
        # HeyGen API setup
        BASE_URL = "https://api.heygen.com"
        HEADERS = {
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Create video payload
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": "Anna_public_3_20240108",
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": summary_text,
                        "voice_id": "2d5b0e6cf36f460aa7fc47e3eee4ba54",
                        "speed": 1.0
                    },
                    "background": {
                        "type": "color",
                        "value": "#ffffff"
                    }
                }
            ],
            "dimension": {
                "width": 1280,
                "height": 720
            }
        }
        
        # Submit video generation request
        response = requests.post(f"{BASE_URL}/v2/video/generate", headers=HEADERS, json=payload)
        response.raise_for_status()
        
        video_id = response.json()["data"]["video_id"]
        
        # Wait for video to be ready
        def wait_for_video(vid):
            url = f"{BASE_URL}/v1/video_status.get?video_id={vid}"
            elapsed = 0
            timeout = 300
            while elapsed < timeout:
                resp = requests.get(url, headers=HEADERS)
                resp.raise_for_status()
                data = resp.json()["data"]
                status = data.get("status")
                if status == "completed":
                    return data["video_url"]
                elif status == "failed":
                    error = data.get("error", "Unknown error")
                    raise RuntimeError(f"Video generation failed: {error}")
                time.sleep(5)
                elapsed += 5
            raise TimeoutError("Timed out waiting for video generation.")
        
        video_url = wait_for_video(video_id)
        
        return {
            "success": True,
            "user_id": data.user_id,
            "date": current_date,
            "data": {
                "tarot_text": summary_text,
                "video_link": video_url
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compatibility-video")
async def compatibility_video(data: TwoPersonInput):
    """
    Generate a compatibility video for two users.
    Takes person details, generates compatibility analysis using OpenAI,
    creates video with HeyGen, and returns text & video link.
    """
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Generate compatibility analysis using OpenAI
        prompt = f"""Generate a detailed compatibility analysis between {data.person1.name} (born {data.person1.birth_date}) and {data.person2.name} (born {data.person2.birth_date}).

        Rules:
        - Cover emotional, intellectual, and physical compatibility — one sentence each, plus a closing advice sentence.
        - Write exactly 4 complete sentences.
        - Every sentence must end with a period.
        - Total length must be between 650-750 characters including spaces.
        - Do NOT cut off mid-sentence.
        - Count characters carefully before responding."""

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,  # 750 chars ≈ ~190 tokens, 300 gives safe buffer
            temperature=0.7
        )

        
        summary_text = response.choices[0].message.content.strip()
        
        # Ensure the text is within character limits
        # char_count = len(summary_text)
        # if char_count < 650:
        #     pass
        # elif char_count > 750:
        #     summary_text = summary_text[:750]
        
        # HeyGen API setup
        BASE_URL = "https://api.heygen.com"
        HEADERS = {
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Create video payload
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": "Anna_public_3_20240108",
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": summary_text,
                        "voice_id": "2d5b0e6cf36f460aa7fc47e3eee4ba54",
                        "speed": 1.0
                    },
                    "background": {
                        "type": "color",
                        "value": "#ffffff"
                    }
                }
            ],
            "dimension": {
                "width": 1280,
                "height": 720
            }
        }
        
        # Submit video generation request
        response = requests.post(f"{BASE_URL}/v2/video/generate", headers=HEADERS, json=payload)
        response.raise_for_status()
        
        video_id = response.json()["data"]["video_id"]
        
        # Wait for video to be ready
        def wait_for_video(vid):
            url = f"{BASE_URL}/v1/video_status.get?video_id={vid}"
            elapsed = 0
            timeout = 300
            while elapsed < timeout:
                resp = requests.get(url, headers=HEADERS)
                resp.raise_for_status()
                data = resp.json()["data"]
                status = data.get("status")
                if status == "completed":
                    return data["video_url"]
                elif status == "failed":
                    error = data.get("error", "Unknown error")
                    raise RuntimeError(f"Video generation failed: {error}")
                time.sleep(5)
                elapsed += 5
            raise TimeoutError("Timed out waiting for video generation.")
        
        video_url = wait_for_video(video_id)
        
        return {
            "success": True,
            "user_id": data.user_id,
            "date": current_date,
            "data": {
                "compatibility_text": summary_text,
                "video_link": video_url
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clarification-card-video")
async def clarification_card_video(data: TarotInput):
    """
    Generate a clarification card video for the user.
    Takes tarot cards, generates short summary using OpenAI,
    creates video with HeyGen, and returns text & video link.
    """
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        cards_str = ", ".join(data.cards)
        # Generate short summary using OpenAI
        prompt = f"""Provide a short summary of the tarot cards: {cards_str}.

        Rules:
        - Write exactly 2 complete sentences.
        - Every sentence must end with a period.
        - Total length must be between 160-180 characters including spaces.
        - Do NOT cut off mid-sentence.
        - Count characters carefully before responding."""

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,  # 180 chars ≈ ~45 tokens, 80 gives safe buffer
            temperature=0.7
        )

        
        summary_text = response.choices[0].message.content.strip()
        
        # Ensure the text is within character limits
        # char_count = len(summary_text)
        # if char_count < 160:
        #     pass
        # elif char_count > 180:
        #     summary_text = summary_text[:180]
        
        # HeyGen API setup
        BASE_URL = "https://api.heygen.com"
        HEADERS = {
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Create video payload
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": "Anna_public_3_20240108",
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": summary_text,
                        "voice_id": "2d5b0e6cf36f460aa7fc47e3eee4ba54",
                        "speed": 1.0
                    },
                    "background": {
                        "type": "color",
                        "value": "#ffffff"
                    }
                }
            ],
            "dimension": {
                "width": 1280,
                "height": 720
            }
        }
        
        # Submit video generation request
        response = requests.post(f"{BASE_URL}/v2/video/generate", headers=HEADERS, json=payload)
        response.raise_for_status()
        
        video_id = response.json()["data"]["video_id"]
        
        # Wait for video to be ready
        def wait_for_video(vid):
            url = f"{BASE_URL}/v1/video_status.get?video_id={vid}"
            elapsed = 0
            timeout = 300
            while elapsed < timeout:
                resp = requests.get(url, headers=HEADERS)
                resp.raise_for_status()
                data = resp.json()["data"]
                status = data.get("status")
                if status == "completed":
                    return data["video_url"]
                elif status == "failed":
                    error = data.get("error", "Unknown error")
                    raise RuntimeError(f"Video generation failed: {error}")
                time.sleep(5)
                elapsed += 5
            raise TimeoutError("Timed out waiting for video generation.")
        
        video_url = wait_for_video(video_id)
        
        return {
            "success": True,
            "user_id": data.user_id,
            "date": current_date,
            "data": {
                "clarification_text": summary_text,
                "video_link": video_url
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
