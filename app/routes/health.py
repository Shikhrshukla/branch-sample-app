from flask import Blueprint, jsonify
from sqlalchemy import text
from app.db import SessionLocal

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health():
    try:
        # Try connecting to the database
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))

        return jsonify({
            "status": "ok",
            "database": "connected"
        }), 200

    except Exception as e:
        # DB unavailable → Healthcheck fails
        return jsonify({
            "status": "error",
            "database": "unavailable",
            "details": str(e)
        }), 500
