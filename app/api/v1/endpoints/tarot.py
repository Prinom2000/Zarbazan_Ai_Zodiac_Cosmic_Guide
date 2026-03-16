"""
Tarot Reading Endpoint
"""

from fastapi import APIRouter, HTTPException
import datetime

from app.schemas import TarotInput, TarotReadingResponse
from app.services import ai_service

router = APIRouter()


@router.post("/tarot-reading", response_model=TarotReadingResponse)
async def tarot_reading(tarot_data: TarotInput):
    """
    Route 6: Tarot Reading
    Returns: Overall message, card explanations, guidance
    """
    try:
        if not tarot_data.cards or len(tarot_data.cards) == 0:
            raise HTTPException(status_code=400, detail="At least one tarot card is required")
        
        cards_list = ", ".join(tarot_data.cards)
        
        # Generate AI tarot reading
        overall_prompt = f"""Provide an overall message for a tarot reading with these cards: {cards_list}.
        Synthesize the cards into a cohesive message about the querent's situation. 4-5 sentences."""
        
        explanation_prompt = f"""Explain each of these tarot cards in the context of this reading: {cards_list}.
        For each card, provide: card name, its meaning in this reading, and what it reveals (2-3 sentences per card).
        Format as: **Card Name**: [Explanation]"""
        
        guidance_prompt = f"""Based on the tarot cards {cards_list}, provide practical guidance and actionable advice.
        What should the person do next? Include 3-4 specific recommendations."""
        
        overall_message = ai_service.generate_content(overall_prompt)
        card_explanations = ai_service.generate_content(explanation_prompt, max_tokens=800)
        guidance = ai_service.generate_content(guidance_prompt)
        
        return {
            "success": True,
            "data": {
                "user_id": tarot_data.user_id,
                "cards_drawn": tarot_data.cards,
                "overall_message": overall_message,
                "card_explanations": card_explanations,
                "guidance": guidance,
                "reading_date": datetime.datetime.now().strftime("%B %d, %Y")
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))