.
├── .env                                    # Environment variables
├── requirements.txt                        # Python dependencies
├── config/
│   └── config.yaml                        # YAML configuration
└── app/
    ├── __init__.py                        # App package init
    ├── main.py                            # FastAPI entry point
    ├── config.py                          # Settings configuration
    ├── api/
    │   ├── __init__.py
    │   └── v1/
    │       ├── __init__.py
    │       └── endpoints/
    │           ├── __init__.py
    │           ├── horoscope.py          # Daily & extended horoscope
    │           ├── compatibility.py       # Compatibility analysis
    │           ├── numerology.py         # Numerology analysis
    │           ├── analysis.py           # Complete life analysis
    │           └── tarot.py              # Tarot reading
    ├── schemas/
    │   └── __init__.py                   # Pydantic models
    ├── services/
    │   ├── __init__.py
    │   └── ai_service.py                 # OpenAI service
    ├── utils/
    │   ├── __init__.py
    │   ├── astrology.py                  # Astrology utilities
    │   ├── numerology.py                 # Numerology utilities
    │   └── compatibility.py              # Compatibility utilities
    └── data/
        └── nakshatra_data.py             # Nakshatra data