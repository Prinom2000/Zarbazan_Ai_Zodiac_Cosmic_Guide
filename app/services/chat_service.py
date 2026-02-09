"""
Chat Service with Memory Context
Provides RAG-enabled chatbot responses for astrology, numerology, and tarot consultations
"""

import os
import requests
import json
from typing import Optional, List, Dict, Any
from openai import OpenAI
from app.config import settings


# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Get BASE_URL from environment
BASE_URL = os.getenv("BASE_URL", "http://72.61.158.79")


def fetch_chat_history(user_id: str, access_token: str) -> List[Dict[str, Any]]:
    """
    Fetch previous conversation history for the user
    """
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"{BASE_URL}/api/v1/ChatHistory?user_id={user_id}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("messages", []) if isinstance(data, dict) else data
    except Exception as e:
        print(f"Error fetching chat history: {str(e)}")
        return []


def fetch_user_data(user_id: str, access_token: str) -> Dict[str, Any]:
    """
    Fetch stored user data including profile information
    """
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"{BASE_URL}/api/v1/data?user_id={user_id}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching user data: {str(e)}")
        return {}


def build_system_prompt(user_data: Dict[str, Any], chat_history: List[Dict[str, Any]]) -> str:
    """
    Build a comprehensive system prompt with user context and astrology knowledge
    """
    system_prompt = """You are an expert astrology and numerology consultant assistant. You have deep knowledge in:

1. **Zodiac Signs & Horoscopes**: Know all 12 zodiac signs, their characteristics, ruling planets, elements, and daily/weekly/monthly/yearly horoscope predictions.

2. **Cosmic Connection**: Understand planetary positions, moon phases, eclipses, retrogrades, and their influence on human lives and relationships.

3. **Tarot Reading**: Proficient in all 78 tarot cards (22 Major Arcana and 56 Minor Arcana), their meanings, reversed interpretations, and spreads.

4. **Compatibility Analysis**: Expert in analyzing astrological compatibility between two people based on zodiac signs, moon signs, rising signs, Venus placements, and Mars placements.

5. **Numerology**: Understand life path numbers, destiny numbers, expression numbers, and their significance in understanding personality and future trends.

Your role is to:
- Provide personalized, thoughtful, and accurate readings based on the user's birth data
- Consider their emotional and spiritual needs
- Give practical guidance with astrological insights
- Be empathetic, encouraging, and non-judgmental
- Explain concepts in a clear and accessible way
- Consider the user's previous conversations and preferences

COMMUNICATION STYLE:
- Be warm, professional, and insightful
- Use the user's name and personal details when relevant
- Provide actionable guidance
- Ask clarifying questions when needed
- Maintain consistency with previous conversations
"""

    # Add user profile context if available
    if user_data:
        system_prompt += "\n\nUSER PROFILE:\n"
        if isinstance(user_data, dict):
            if "name" in user_data:
                system_prompt += f"- Name: {user_data['name']}\n"
            if "zodiac_sign" in user_data:
                system_prompt += f"- Zodiac Sign: {user_data['zodiac_sign']}\n"
            if "birth_date" in user_data:
                system_prompt += f"- Birth Date: {user_data['birth_date']}\n"
            if "birth_time" in user_data:
                system_prompt += f"- Birth Time: {user_data['birth_time']}\n"
            if "birth_location" in user_data:
                system_prompt += f"- Birth Location: {user_data['birth_location']}\n"
            if "moon_sign" in user_data:
                system_prompt += f"- Moon Sign: {user_data['moon_sign']}\n"
            if "rising_sign" in user_data:
                system_prompt += f"- Rising Sign: {user_data['rising_sign']}\n"
            if "life_path_number" in user_data:
                system_prompt += f"- Life Path Number: {user_data['life_path_number']}\n"

    # Add conversation context if available
    if chat_history:
        system_prompt += "\n\nRECENT CONVERSATION HISTORY:\n"
        recent_messages = chat_history[-5:]  # Get last 5 messages for context
        for idx, msg in enumerate(recent_messages):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            system_prompt += f"- {role.upper()}: {content[:100]}...\n" if len(content) > 100 else f"- {role.upper()}: {content}\n"

    system_prompt += "\nProvide thoughtful, accurate, and personalized responses based on the above context."
    
    return system_prompt


async def chat_with_memory_contaxt(
    user_id: str,
    message: str,
    access_token: Optional[str] = None
) -> str:
    """
    Generate a response using OpenAI with user context from chat history and stored data
    
    Args:
        user_id: The user's unique identifier
        message: The user's current message
        access_token: Access token for API authentication
    
    Returns:
        The assistant's response message
    """
    try:
        # Fetch user context data
        user_data = {}
        chat_history = []
        
        if access_token:
            user_data = fetch_user_data(user_id, access_token)
            chat_history = fetch_chat_history(user_id, access_token)
        
        # Build system prompt with context
        system_prompt = build_system_prompt(user_data, chat_history)
        
        # Prepare messages for OpenAI API
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
        
        # Add chat history to messages (if available)
        if chat_history:
            for msg in chat_history[-10:]:  # Include last 10 messages for context
                if "role" in msg and "content" in msg:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
            top_p=0.9,
        )
        
        # Extract and return the response
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error in chat_with_memory_contaxt: {str(e)}")
        return f"I apologize, but I encountered an error: {str(e)}. Please try again."
