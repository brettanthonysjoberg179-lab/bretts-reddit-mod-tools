"""Mod Log — auth and API routes."""
from flask import Blueprint, redirect, url_for, session, request, jsonify
from shared.auth.oauth2 import generate_state, handle_callback, reddit_request

auth_bp = Blueprint("log_auth", __name__)
api_bp = Blueprint("log_api", __name__)

@auth_bp.route("/mod-log/login")
def login():
    state = generate_state()
    session["oauth_state"] = state
    config = __import__("shared.config.settings", fromlist=["get_config"]).get_config()
    auth_url = (
        f"https://www.reddit.com/api/v1/authorize"
        f"?client_id={config['REDDIT_CLIENT_ID']}"
        f"&response_type=code"
        f"&state={state}"
        f"&redirect_uri={config['REDDIT_REDIRECT_URI']}"
        f"&duration=permanent"
        f"&scope=read+modlog+modposts"
    )
    return redirect(auth_url)

@auth_bp.route("/mod-log/callback")
def callback():
    code = request.args.get("code")
    token_data = handle_callback(code)
    return redirect("/mod-log") if token_data else ("Auth failed", 401)

@api_bp.route("/mod-log/actions", methods=["GET"])
def get_actions():
    sub = request.args.get("subreddit", "mod")
    count = request.args.get("count", 50)
    return jsonify(reddit_request(f"/r/{sub}/about/log", params={"limit": count}))

@api_bp.route("/mod-log/analytics", methods=["GET"])
def analytics():
    sub = request.args.get("subreddit", "mod")
    # Basic analytics: aggregate by action type
    actions = reddit_request(f"/r/{sub}/about/log", params={"limit": 100})
    return jsonify({"subreddit": sub, "raw": actions})
