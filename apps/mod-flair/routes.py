"""Mod Flair routes."""
from flask import Blueprint, render_template_string, session
from shared.auth.oauth2 import login_required

main_bp = Blueprint("mod_flair", __name__)

@main_bp.route("/mod-flair")
@login_required
def index():
    return render_template_string("""
    <h1>Mod Flair</h1>
    <p>Manage subreddit flair assignments.</p>
    """, session=session)
