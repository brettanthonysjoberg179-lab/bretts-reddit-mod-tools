"""Mod Mail — auth and API routes."""
from flask import Blueprint, redirect, url_for, session, request, jsonify
from shared.auth.oauth2 import generate_state, handle_callback, reddit_request

auth_bp = Blueprint("mail_auth", __name__)
api_bp = Blueprint("mail_api", __name__)

@auth_bp.route("/mod-mail/login")
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
        f"&scope=read+modmail"
    )
    return redirect(auth_url)

@auth_bp.route("/mod-mail/callback")
def callback():
    code = request.args.get("code")
    token_data = handle_callback(code)
    return redirect("/mod-mail") if token_data else ("Auth failed", 401)

@api_bp.route("/mod-mail/inbox", methods=["GET"])
def get_inbox():
    sub = request.args.get("subreddit", "mod")
    return jsonify(reddit_request(f"/r/{sub}/message/inbox"))

@api_bp.route("/mod-mail/send", methods=["POST"])
def send():
    sub = request.json.get("subreddit")
    to = request.json.get("to")
    body = request.json.get("body")
    return jsonify(reddit_request(f"/r/{sub}/api/mail", method="POST", data={"to": to, "body": body}))

@api_bp.route("/mod-mail/reply", methods=["POST"])
def reply():
    thread_id = request.json.get("id")
    body = request.json.get("body")
    return jsonify(reddit_request(f"/r/mod/message/reply/{thread_id}", method="POST", data={"body": body}))
