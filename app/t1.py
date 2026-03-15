import os
import requests
import time

# Get API key from environment variable
api_key = os.getenv("HEYGEN_API_KEY")
print(f"Using API Key: {api_key}")

from config import settings

heygen_key = settings.HEYGEN_API_KEY
print(heygen_key)