"""Mod Mail routes."""
from flask import Blueprint, render_template_string, session
from shared.auth.oauth2 import login_required

main_bp = Blueprint("mod_mail", __name__)

@main_bp.route("/mod-mail")
@login_required
def index():
    return render_template_string("""
    <h1>Mod Mail</h1>
    <p>Read and respond to mod mail.</p>
    """, session=session)
