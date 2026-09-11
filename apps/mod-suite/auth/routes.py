"""Mod Suite — authentication routes."""
from flask import Blueprint, redirect, url_for, session, request
from shared.auth.oauth2 import generate_state, handle_callback

auth_bp = Blueprint("suite_auth", __name__)

@auth_bp.route("/mod-suite/login")
def login():
    state = generate_state()
    session["oauth_state"] = state
    auth_url = (
        f"https://www.reddit.com/api/v1/authorize"
        f"?client_id={__import__('shared.config.settings', fromlist=['get_config']).get_config()['REDDIT_CLIENT_ID']}"
        f"&response_type=code"
        f"&state={state}"
        f"&redirect_uri={__import__('shared.config.settings', fromlist=['get_config']).get_config()['REDDIT_REDIRECT_URI']}"
        f"&duration=permanent"
        f"&scope=read+modposts+modconfig+modlog+modflair+modcontributors+modmail+modothers"
    )
    return redirect(auth_url)

@auth_bp.route("/mod-suite/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Missing code", 400
    token_data = handle_callback(code)
    if token_data:
        return redirect("/mod-suite")
    return "Authentication failed", 401

@auth_bp.route("/mod-suite/logout")
def logout():
    session.clear()
    return redirect("/")
