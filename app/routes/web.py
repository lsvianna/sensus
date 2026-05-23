from flask import Blueprint, render_template


web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    return render_template("index.html")


@web_bp.route("/<path:path>")
def spa_fallback(path):
    if path.startswith("api/"):
        return {"error": "Not found"}, 404
    return render_template("index.html")
