import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
BASE_URL = "https://api.heygen.com"

HEADERS = {
    "X-Api-Key": HEYGEN_API_KEY,
    "Content-Type": "application/json"
}

# ─────────────────────────────────────────────
# CONFIGURE YOUR VIDEO HERE
# ─────────────────────────────────────────────
TEXT_INPUT = """
Hello! Welcome to our platform. 
This is an AI-generated video using HeyGen.
You can replace this text with anything you want.
"""

AVATAR_ID = "Anna_public_3_20240108"   # Free HeyGen stock avatar
VOICE_ID  = "2d5b0e6cf36f460aa7fc47e3eee4ba54"  # English female voice
BACKGROUND_COLOR = "#ffffff"           # White background
VIDEO_WIDTH  = 1280
VIDEO_HEIGHT = 720
# ─────────────────────────────────────────────


def create_video(text: str) -> str:
    """Submit a text-to-video generation request and return video_id."""
    url = f"{BASE_URL}/v2/video/generate"

    payload = {
    "video_inputs": [
        {
            "character": {
                "type": "avatar",
                "avatar_id": AVATAR_ID,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": text,
                "voice_id": VOICE_ID,
                "speed": 1.0
            },
            "background": {
                "type": "color", 
                "value": BACKGROUND_COLOR
            }
        }
    ],
    "dimension": {
        "width": VIDEO_WIDTH,
        "height": VIDEO_HEIGHT
    }
    # "test": True  ← এটা remove করো, কোনো কাজ নেই
}

    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()

    data = response.json()
    video_id = data["data"]["video_id"]
    print(f"✅ Video submitted! video_id: {video_id}")
    return video_id


def wait_for_video(video_id: str, poll_interval: int = 5, timeout: int = 300) -> str:
    """Poll HeyGen until the video is ready, then return the download URL."""
    url = f"{BASE_URL}/v1/video_status.get?video_id={video_id}"
    elapsed = 0

    print("⏳ Waiting for video to render", end="", flush=True)

    while elapsed < timeout:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        data = response.json()["data"]
        status = data.get("status")

        if status == "completed":
            print("\n🎉 Video is ready!")
            return data["video_url"]
        elif status == "failed":
            error = data.get("error", "Unknown error")
            raise RuntimeError(f"❌ Video generation failed: {error}")
        else:
            print(".", end="", flush=True)
            time.sleep(poll_interval)
            elapsed += poll_interval

    raise TimeoutError("⏰ Timed out waiting for video.")


def download_video(video_url: str, output_path: str = "output_video.mp4") -> None:
    """Download the finished video to a local file."""
    print(f"⬇️  Downloading video to '{output_path}'...")
    response = requests.get(video_url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✅ Saved to: {output_path}")


def list_avatars() -> None:
    """Helper: print available avatar IDs from your HeyGen account."""
    url = f"{BASE_URL}/v2/avatars"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    avatars = response.json()["data"]["avatars"]
    print("\n📋 Available Avatars:")
    for a in avatars:
        print(f"  - {a['avatar_name']}: {a['avatar_id']}")


def list_voices() -> None:
    """Helper: print available voice IDs."""
    url = f"{BASE_URL}/v2/voices"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    voices = response.json()["data"]["voices"]
    print("\n🎙️  Available Voices (first 20):")
    for v in voices[:20]:
        print(f"  - [{v['language']}] {v['name']}: {v['voice_id']}")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    if not HEYGEN_API_KEY:
        raise ValueError("HEYGEN_API_KEY not found in .env file!")

    print(f"🔑 Using API Key: {HEYGEN_API_KEY[:50]}...")

    # Uncomment these to explore available avatars & voices:
    # list_avatars()
    # list_voices()

    # Generate the video
    video_id  = create_video(TEXT_INPUT)
    video_url = wait_for_video(video_id)
    download_video(video_url, output_path="my_heygen_video.mp4")