import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the application."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-transcription-app')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True' 