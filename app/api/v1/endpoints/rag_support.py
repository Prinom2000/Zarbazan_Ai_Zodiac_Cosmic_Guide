"""
RAG Support Endpoint - Chatbot with Memory and Context
Provides intelligent responses using chat history, user data, and OpenAI
"""

from fastapi import APIRouter, Query, HTTPException
from app.services.chat_service import chat_with_memory_contaxt
import os
import datetime

router = APIRouter()


@router.post("/chat")
async def chat(
    user_id: str = Query(..., description="User ID for personalized responses"),
    message: str = Query(..., description="User's message to the chatbot"),
    access_token: str = Query(..., description="User access token for fetching context")
):
    """
    Chat endpoint with context-aware responses
    
    - Fetches previous chat history from {{BASE_URL}}/api/v1/ChatHistory
    - Fetches user data from {{BASE_URL}}/api/v1/data
    - Generates personalized response using OpenAI with astrology knowledge
    
    Args:
        user_id: Unique user identifier
        message: User's message/query
        access_token: Authentication token for accessing user context
    
    Returns:
        JSON response with the chatbot's reply
    """
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            raise HTTPException(status_code=400, detail="user_id cannot be empty")
        
        if not message or not message.strip():
            raise HTTPException(status_code=400, detail="message cannot be empty")
        
        if not access_token or not access_token.strip():
            raise HTTPException(status_code=401, detail="access_token is required")
        
        # Get response from OpenAI with memory and context
        response = await chat_with_memory_contaxt(
            user_id=user_id,
            message=message,
            access_token=access_token
        )
        
        return {
            "success": True,
            "response": response,
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )







