from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "UP",
        "message": "Student API is running"
    }), 200
