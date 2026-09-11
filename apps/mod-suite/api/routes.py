"""Mod Suite — API routes for mod actions."""
from flask import Blueprint, jsonify, request
from shared.auth.oauth2 import login_required, reddit_request

api_bp = Blueprint("suite_api", __name__)

@api_bp.route("/mod-suite/api/approve", methods=["POST"])
@login_required
def approve():
    post_id = request.json.get("id")
    return jsonify(reddit_request(f"/api/approve", method="POST", data={"id": post_id}))

@api_bp.route("/mod-suite/api/remove", methods=["POST"])
@login_required
def remove():
    post_id = request.json.get("id")
    spam = request.json.get("spam", False)
    return jsonify(reddit_request(f"/api/remove", method="POST", data={"id": post_id, "spam": str(spam).lower()}))

@api_bp.route("/mod-suite/api/ban", methods=["POST"])
@login_required
def ban():
    sub = request.json.get("subreddit")
    user = request.json.get("username")
    reason = request.json.get("reason", "")
    return jsonify(reddit_request(f"/r/{sub}/api/friend", method="POST", data={"name": user, "type": "banned", "reason": reason}))

@api_bp.route("/mod-suite/api/unban", methods=["POST"])
@login_required
def unban():
    sub = request.json.get("subreddit")
    user = request.json.get("username")
    return jsonify(reddit_request(f"/r/{sub}/api/friend", method="POST", data={"name": user, "type": "unbanned"}))

@api_bp.route("/mod-suite/api/modqueue", methods=["GET"])
@login_required
def modqueue():
    sub = request.args.get("subreddit", "mod")
    return jsonify(reddit_request(f"/r/{sub}/about/modqueue"))
