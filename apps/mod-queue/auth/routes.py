"""Mod Queue — auth and API routes."""
from flask import Blueprint, redirect, url_for, session, request, jsonify
from shared.auth.oauth2 import generate_state, handle_callback, reddit_request

auth_bp = Blueprint("queue_auth", __name__)
api_bp = Blueprint("queue_api", __name__)

@auth_bp.route("/mod-queue/login")
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
        f"&scope=read+modposts+modothers"
    )
    return redirect(auth_url)

@auth_bp.route("/mod-queue/callback")
def callback():
    code = request.args.get("code")
    token_data = handle_callback(code)
    return redirect("/mod-queue") if token_data else ("Auth failed", 401)

@api_bp.route("/mod-queue/queue", methods=["GET"])
def get_queue():
    sub = request.args.get("subreddit", "mod")
    return jsonify(reddit_request(f"/r/{sub}/about/modqueue"))

@api_bp.route("/mod-queue/approve", methods=["POST"])
def approve():
    post_id = request.json.get("id")
    return jsonify(reddit_request("/api/approve", method="POST", data={"id": post_id}))

@api_bp.route("/mod-queue/remove", methods=["POST"])
def remove():
    post_id = request.json.get("id")
    return jsonify(reddit_request("/api/remove", method="POST", data={"id": post_id}))
