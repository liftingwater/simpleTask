import os

class Config:
    # Frontend theme selection - set to None for API-only mode
    FRONTEND_THEME = os.environ.get('FRONTEND_THEME', 'basic')

    # Flask config
    DEBUG = os.environ.get('FLASK_DEBUG', True)

