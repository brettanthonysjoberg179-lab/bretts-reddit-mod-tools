"""Mod Queue routes."""
from flask import Blueprint, render_template_string, session
from shared.auth.oauth2 import login_required

main_bp = Blueprint("mod_queue", __name__)

@main_bp.route("/mod-queue")
@login_required
def index():
    return render_template_string("""
    <h1>Mod Queue</h1>
    <p>Review items pending moderation.</p>
    <div id="queue-container">Loading...</div>
    """, session=session)
