"""OAuth2 authentication module — login, callback, token refresh."""
import secrets
import time
from functools import wraps

import requests
try:
    from flask import session, redirect, url_for, request, jsonify
except ImportError:
    session = {}
    redirect = lambda x: x
    url_for = lambda x: x
    request = type("Request", (), {"args": {}, "json": {}})()
    jsonify = lambda x: x
from shared.api.client import reddit_request

def generate_state():
    """Generate a random state string for CSRF protection."""
    return secrets.token_urlsafe(16)

def build_auth_url(state, scopes=None):
    """Build the Reddit OAuth2 authorization URL."""
    if scopes is None:
        scopes = "read modposts modconfig modlog modflair modcontributors modmail modothers"
    from shared.config.settings import get_config
    config = get_config()
    return (
        f"https://www.reddit.com/api/v1/authorize"
        f"?client_id={config['REDDIT_CLIENT_ID']}"
        f"&response_type=code"
        f"&state={state}"
        f"&redirect_uri={config['REDDIT_REDIRECT_URI']}"
        f"&duration=permanent"
        f"&scope={scopes}"
    )

def handle_callback(code):
    """Exchange authorization code for access/refresh tokens."""
    config = get_config()
    auth = requests.auth.HTTPBasicAuth(config['REDDIT_CLIENT_ID'], config['REDDIT_CLIENT_SECRET'])
    data = {"grant_type": "authorization_code", "code": code, "redirect_uri": config['REDDIT_REDIRECT_URI']}
    headers = {"User-Agent": "BrettModTools/1.0"}
    resp = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    if resp.status_code == 200:
        token_data = resp.json()
        session["access_token"] = token_data["access_token"]
        session["refresh_token"] = token_data.get("refresh_token")
        session["token_expires"] = time.time() + token_data.get("expires_in", 3600)
        return token_data
    return None

def refresh_access_token():
    """Refresh an expired access token using the refresh token."""
    config = get_config()
    refresh_token = session.get("refresh_token")
    if not refresh_token:
        return None
    auth = requests.auth.HTTPBasicAuth(config['REDDIT_CLIENT_ID'], config['REDDIT_CLIENT_SECRET'])
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    headers = {"User-Agent": "BrettModTools/1.0"}
    resp = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    if resp.status_code == 200:
        token_data = resp.json()
        session["access_token"] = token_data["access_token"]
        session["token_expires"] = time.time() + token_data.get("expires_in", 3600)
        return token_data["access_token"]
    return None

def login_required(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "access_token" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated
