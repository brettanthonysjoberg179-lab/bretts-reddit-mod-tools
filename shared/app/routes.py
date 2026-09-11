"""Shared Flask routes — homepage, health check."""
from flask import Blueprint, render_template_string, jsonify

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template_string("""
    <h1>Brett's Reddit Mod Tools</h1>
    <p>Select a tool from the navigation above.</p>
    """)

@main_bp.route("/health")
def health():
    return jsonify({"status": "ok"})
