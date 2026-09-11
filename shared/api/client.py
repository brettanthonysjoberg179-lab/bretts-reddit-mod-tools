"""Reddit API request helper with rate limiting and auto-refresh."""
import time
import requests
from functools import wraps

try:
    from flask import session
except ImportError:
    session = {}
from shared.config.settings import get_config

class RateLimiter:
    """Simple rate limiter for Reddit API calls."""
    def __init__(self, max_requests=60, per_seconds=60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.timestamps = []

    def acquire(self):
        """Wait if necessary to stay under rate limit."""
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t < self.per_seconds]
        if len(self.timestamps) >= self.max_requests:
            sleep_time = self.per_seconds - (now - self.timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
            now = time.time()
            self.timestamps = [t for t in self.timestamps if now - t < self.per_seconds]
        self.timestamps.append(now)

_rate_limiter = RateLimiter()

def reddit_request(endpoint, method="GET", data=None, token=None, params=None):
    """
    Make an authenticated request to the Reddit OAuth API.
    Auto-refreshes token on 401.
    """
    if token is None:
        from shared.auth.oauth2 import refresh_access_token, session
        token = session.get("access_token")
    if not token:
        return None

    config = get_config()
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "BrettModTools/1.0"
    }
    url = f"https://oauth.reddit.com{endpoint}"

    try:
        _rate_limiter.acquire()
        if method == "GET":
            resp = requests.get(url, headers=headers, params=params or {}, timeout=15)
        elif method == "POST":
            resp = requests.post(url, headers=headers, data=data or {}, timeout=15)
        elif method == "DELETE":
            resp = requests.delete(url, headers=headers, data=data or {}, timeout=15)
        else:
            return None

        if resp.status_code == 401:
            new_token = refresh_access_token()
            if new_token:
                headers["Authorization"] = f"Bearer {new_token}"
                if method == "GET":
                    resp = requests.get(url, headers=headers, params=params or {}, timeout=15)
                else:
                    resp = requests.post(url, headers=headers, data=data or {}, timeout=15)
            else:
                return None

        if resp.status_code == 200:
            return resp.json()
        return None
    except requests.RequestException:
        return None
