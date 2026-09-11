"""Mod Suite routes — dashboard, overview, stats."""
from flask import Blueprint, render_template_string, session, jsonify
from shared.auth.oauth2 import login_required, reddit_request

main_bp = Blueprint("mod_suite", __name__)

@main_bp.route("/mod-suite")
@login_required
def dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>Mod Suite</title></head>
    <body>
        <h1>Mod Suite Dashboard</h1>
        <p>Welcome, {{ session.get('reddit_username', 'Mod') }}</p>
        <nav>
            <a href="/mod-suite/queue">Mod Queue</a> |
            <a href="/mod-suite/log">Mod Log</a> |
            <a href="/mod-suite/mail">Mod Mail</a> |
            <a href="/mod-suite/flair">Flair</a>
        </nav>
    </body>
    </html>
    """, session=session)

@main_bp.route("/mod-suite/stats")
@login_required
def stats():
    # Fetch subreddit info as a demo
    sub = session.get("mod_subreddit", "mod")
    result = reddit_request(f"/r/{sub}/about")
    return jsonify(result or {"error": "Could not fetch stats"})
