"""
AI Service for generating content using OpenAI
"""

from openai import OpenAI
from app.config import settings


class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_content(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate AI content using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert astrologer and spiritual advisor. Provide insightful, personalized, and positive guidance."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Unable to generate content at this time. Error: {str(e)}"


# Global AI service instance
ai_service = AIService()