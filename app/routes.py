from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from .database import db
from .logger import setup_logger
from .models import Student

logger = setup_logger()

student_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/api/v1/students",
)


# CREATE student
@student_bp.route("", methods=["POST"])
def create_student():
    data = request.get_json(silent=True)

    if not data:
        logger.warning("Create student request with empty or invalid JSON")
        return (
            jsonify(
                {
                    "error": (
                        "Request body is required and must be in JSON format"
                    )
                }
            ),
            400,
        )

    required_fields = ["name", "age", "email"]

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        message = (
            f"Missing required fields: {', '.join(missing_fields)}"
        )
        logger.warning(message)

        return jsonify({"error": message}), 400

    logger.info("Creating student: %s", data.get("email"))

    student = Student(
        name=data["name"],
        age=data["age"],
        email=data["email"],
    )

    try:
        db.session.add(student)
        db.session.commit()

        logger.info(
            "Student created successfully with ID %s",
            student.id,
        )

        return jsonify(student.to_dict()), 201

    except IntegrityError as error:
        db.session.rollback()

        logger.warning(
            "Duplicate email attempted: %s. Error: %s",
            data["email"],
            error,
        )

        return jsonify({"error": "Email already exists"}), 409

    except Exception as error:
        db.session.rollback()

        logger.exception(
            "Unexpected error creating student: %s",
            error,
        )

        return jsonify({"error": "Internal server error"}), 500


# GET all students
@student_bp.route("", methods=["GET"])
def get_students():
    logger.info("Fetching all students")

    students = Student.query.all()

    return jsonify(
        [student.to_dict() for student in students]
    ), 200


# GET student by ID
@student_bp.route("/<int:student_id>", methods=["GET"])
def get_student(student_id):
    logger.info("Fetching student with ID %s", student_id)

    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student.to_dict()), 200


# UPDATE student
@student_bp.route("/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    logger.info("Updating student with ID %s", student_id)

    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True)

    if data is None:
        logger.warning(
            "Update request for student %s has empty or invalid JSON",
            student_id,
        )

        return (
            jsonify(
                {
                    "error": (
                        "Request body is required and must be in JSON format"
                    )
                }
            ),
            400,
        )

    allowed_fields = ["name", "age", "email"]

    if not any(field in data for field in allowed_fields):
        logger.warning(
            "Update request for student %s has no updatable fields",
            student_id,
        )

        return (
            jsonify(
                {
                    "error": (
                        "At least one field "
                        "(name, age, email) must be provided"
                    )
                }
            ),
            400,
        )

    if "name" in data:
        student.name = data["name"]

    if "age" in data:
        student.age = data["age"]

    if "email" in data:
        student.email = data["email"]

    try:
        db.session.commit()

        logger.info(
            "Student %s updated successfully",
            student_id,
        )

        return jsonify(student.to_dict()), 200

    except IntegrityError as error:
        db.session.rollback()

        logger.warning(
            "Duplicate email attempted for student %s: %s. Error: %s",
            student_id,
            data.get("email"),
            error,
        )

        return jsonify({"error": "Email already exists"}), 409

    except Exception as error:
        db.session.rollback()

        logger.exception(
            "Unexpected error updating student %s: %s",
            student_id,
            error,
        )

        return jsonify({"error": "Internal server error"}), 500


# DELETE student
@student_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    logger.info("Deleting student with ID %s", student_id)

    try:
        db.session.delete(student)
        db.session.commit()

        logger.info(
            "Student %s deleted successfully",
            student_id,
        )

        return jsonify(
            {"message": "Student deleted successfully"}
        ), 200

    except Exception as error:
        db.session.rollback()

        logger.exception(
            "Unexpected error deleting student %s: %s",
            student_id,
            error,
        )

        return jsonify({"error": "Internal server error"}), 500
