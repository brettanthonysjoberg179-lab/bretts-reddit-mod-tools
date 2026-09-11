"""Shared configuration loader."""
import os
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

def get_config():
    """Return the current configuration dict."""
    return {
        "REDDIT_CLIENT_ID": os.getenv("REDDIT_CLIENT_ID", ""),
        "REDDIT_CLIENT_SECRET": os.getenv("REDDIT_CLIENT_SECRET", ""),
        "REDDIT_REDIRECT_URI": os.getenv("REDDIT_REDIRECT_URI", "http://localhost:5000/callback"),
        "FLASK_ENV": os.getenv("FLASK_ENV", "development"),
        "FLASK_DEBUG": os.getenv("FLASK_DEBUG", "1") == "1",
        "SECRET_KEY": os.getenv("SECRET_KEY", "change-me"),
        "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///mod_tools.db"),
    }

def load_config(config_path=None):
    """Load configuration into a Flask-compatible dict."""
    config = get_config()
    return {
        "SECRET_KEY": config["SECRET_KEY"],
        "SQLALCHEMY_DATABASE_URI": config["DATABASE_URL"],
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "REDDIT_CLIENT_ID": config["REDDIT_CLIENT_ID"],
        "REDDIT_CLIENT_SECRET": config["REDDIT_CLIENT_SECRET"],
        "REDDIT_REDIRECT_URI": config["REDDIT_REDIRECT_URI"],
    }
