import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('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')
    OPENAI_MODEL = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE = 0.3
    
    # Content Moderation Thresholds
    TOXICITY_THRESHOLD = 0.7
    HATE_SPEECH_THRESHOLD = 0.8
    EXPLICIT_CONTENT_THRESHOLD = 0.85
    
    # Flask Configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')