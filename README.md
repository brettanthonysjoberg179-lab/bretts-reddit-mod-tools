# Brett's Reddit Mod Tools

A collection of Reddit moderation tools built with Flask + Reddit's OAuth2 API.
Each tool is an independent modular app under `apps/`.

## Project Structure

```
bretts-reddit-mod-tools/
├── shared/          # Reusable packages (auth, API client, config)
│   ├── app/         # Flask app factory, extensions, blueprints
│   ├── auth/        # OAuth2 flow, token storage, refresh
│   ├── api/         # Reddit API request helper, rate limiter
│   └── config/      # Shared config, env parsing
├── apps/            # Independent Reddit mod tool apps
│   ├── mod-suite/   # All-in-one mod dashboard
│   ├── mod-queue/   # Moderation queue viewer & processor
│   ├── mod-log/     # Moderation log viewer & analytics
│   ├── mod-mail/    # Mod mail reader & responder
│   ├── mod-flair/   # Flair management tool
│   └── ...          # Future tools
├── scripts/         # Utility scripts (setup, migrations, seed)
├── tests/           # Shared and per-app test suites
├── requirements.txt # Python dependencies
├── .env.example     # Environment template
└── .gitignore
```

## Stack

- **Flask 3.x** — Web framework
- **requests** — Reddit API calls (not PRAW — direct API for control)
- **sqlite3** — User/data storage
- **Gunicorn** — Production server

## Quick Start

1. Copy `.env.example` to `.env` and fill in your Reddit app credentials
2. `pip install -r requirements.txt`
3. `python scripts/setup.py` — initialize shared DB and config
4. Run any app: `python apps/mod-suite/app.py`

## Apps

| App | Purpose |
|-----|---------|
| **mod-suite** | All-in-one mod dashboard |
| **mod-queue** | Mod queue viewer & bulk actions |
| **mod-log** | Mod log viewer & analytics |
| **mod-mail** | Mod mail inbox & auto-respond |
| **mod-flair** | Flair assignment & bulk editing |

## Reddit API

- Base: `https://oauth.reddit.com`
- Auth: `https://www.reddit.com/api/v1`
- Rate limit: 60 req/min authenticated, 10/min unauthenticated
- Register apps at: https://www.reddit.com/prefs/apps

## License

Fair Dinkum Publishing — Internal use
