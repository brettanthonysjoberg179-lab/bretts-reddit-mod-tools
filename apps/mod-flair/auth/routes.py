"""Mod Flair — auth and API routes."""
from flask import Blueprint, redirect, url_for, session, request, jsonify
from shared.auth.oauth2 import generate_state, handle_callback, reddit_request

auth_bp = Blueprint("flair_auth", __name__)
api_bp = Blueprint("flair_api", __name__)

@auth_bp.route("/mod-flair/login")
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
        f"&scope=read+modflair+modposts"
    )
    return redirect(auth_url)

@auth_bp.route("/mod-flair/callback")
def callback():
    code = request.args.get("code")
    token_data = handle_callback(code)
    return redirect("/mod-flair") if token_data else ("Auth failed", 401)

@api_bp.route("/mod-flair/list", methods=["GET"])
def get_flairs():
    sub = request.args.get("subreddit", "mod")
    return jsonify(reddit_request(f"/r/{sub}/api/flairlist"))

@api_bp.route("/mod-flair/assign", methods=["POST"])
def assign_flair():
    sub = request.json.get("subreddit")
    user = request.json.get("user")
    text = request.json.get("text", "")
    css_class = request.json.get("css_class", "")
    return jsonify(reddit_request(f"/r/{sub}/api/flair", method="POST", data={"name": user, "text": text, "css_class": css_class}))

@api_bp.route("/mod-flair/bulk", methods=["POST"])
def bulk_assign():
    sub = request.json.get("subreddit")
    users = request.json.get("users", [])
    text = request.json.get("text", "")
    results = []
    for user in users:
        result = reddit_request(f"/r/{sub}/api/flair", method="POST", data={"name": user, "text": text})
        results.append({"user": user, "result": result})
    return jsonify({"subreddit": sub, "results": results})
