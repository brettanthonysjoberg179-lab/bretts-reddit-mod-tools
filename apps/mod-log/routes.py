"""Mod Log routes."""
from flask import Blueprint, render_template_string, session
from shared.auth.oauth2 import login_required

main_bp = Blueprint("mod_log", __name__)

@main_bp.route("/mod-log")
@login_required
def index():
    return render_template_string("""
    <h1>Mod Log</h1>
    <p>View and analyze moderation actions.</p>
    """, session=session)
