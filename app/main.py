"""
FastAPI Astrology & Numerology API - Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import (
    horoscope,
    compatibility,
    numerology,
    analysis,
    tarot,
    rag_support
)
from app.config import settings
import datetime

# Initialize FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Complete astrology, numerology, and tarot reading service",
    version=settings.VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(horoscope.router, prefix="/api", tags=["Horoscope"])
app.include_router(compatibility.router, prefix="/api", tags=["Compatibility"])
app.include_router(numerology.router, prefix="/api", tags=["Numerology"])
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(tarot.router, prefix="/api", tags=["Tarot"])
app.include_router(rag_support.router, prefix="/api/v1", tags=["Chat & RAG Support"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Astrology & Numerology API",
        "version": settings.VERSION,
        "endpoints": [
            "/api/daily-horoscope",
            "/api/extended-horoscope",
            "/api/compatibility",
            "/api/numerology",
            "/api/complete-analysis",
            "/api/tarot-reading",
            "/api/v1/chat"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)