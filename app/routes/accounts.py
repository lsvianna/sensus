from flask import request, jsonify

from app.models import db, InstagramAccount, User
from app.routes import api_bp


@api_bp.route("/accounts", methods=["GET"])
def get_accounts():
    """List a user's Instagram accounts."""

    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    accounts = InstagramAccount.query.filter_by(user_id=user_id).order_by(InstagramAccount.created_at.desc()).all()

    return jsonify({
        "accounts": [{
            "id": acc.id,
            "username": acc.username,
            "display_name": acc.display_name,
            "followers_count": acc.followers_count,
            "posts_count": len(acc.posts),
        } for acc in accounts]
    }), 200


@api_bp.route("/accounts", methods=["POST"])
def add_account():
    """Add an Instagram account to monitor."""

    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    username = (data.get("instagram_username") or "").strip().lstrip("@")

    if not user_id or not username:
        return jsonify({"error": "user_id and instagram_username are required"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    existing = InstagramAccount.query.filter_by(user_id=user_id, username=username).first()
    if existing:
        return jsonify({"error": "Account already monitored"}), 400

    account = InstagramAccount(
        user_id=user_id,
        instagram_id=f"local_{user_id}_{username}",
        username=username,
        display_name=data.get("display_name") or username,
        followers_count=data.get("followers_count") or 0,
        bio=data.get("bio") or "",
    )

    db.session.add(account)
    db.session.commit()

    return jsonify({"message": "Account added", "account_id": account.id}), 201


@api_bp.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """Get account details."""

    account = db.session.get(InstagramAccount, account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({
        "id": account.id,
        "username": account.username,
        "display_name": account.display_name,
        "followers_count": account.followers_count,
        "bio": account.bio,
        "posts_count": len(account.posts),
        "last_sync": account.last_sync.isoformat() if account.last_sync else None,
    }), 200
