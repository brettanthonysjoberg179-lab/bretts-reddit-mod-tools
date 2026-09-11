"""Setup script for bretts-reddit-mod-tools."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

def setup():
    """Initialize the project: create directories, copy .env, init DB."""
    # Ensure .env exists
    env_path = ROOT / ".env"
    if not env_path.exists():
        import shutil
        shutil.copy(ROOT / ".env.example", env_path)
        print("Created .env from .env.example — edit it with your Reddit credentials.")

    # Ensure shared config exists
    config_dir = ROOT / "shared" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Create shared DB
    db_path = ROOT / "mod_tools.db"
    if not db_path.exists():
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reddit_username TEXT UNIQUE NOT NULL,
                access_token TEXT,
                refresh_token TEXT,
                token_expires TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS mod_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                subreddit TEXT NOT NULL,
                action_type TEXT NOT NULL,
                target_type TEXT,
                target_id TEXT,
                target_author TEXT,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()
        print(f"Created shared database at {db_path}")

    print("Setup complete. Configure your .env and run an app.")

if __name__ == "__main__":
    setup()
