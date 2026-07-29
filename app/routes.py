from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from .database import db
from .models import Student
from .logger import setup_logger
logger = setup_logger()

student_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/api/v1/students"
)


# CREATE student
@student_bp.route("", methods=["POST"])
def create_student():
    data = request.get_json(silent=True)
    if not data:
        logger.warning("Create student request with empty or invalid JSON")
        return jsonify({
            "error": "Request body is required and must be in JSON format"
        }), 400

    required_fields = ["name", "age", "email"]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        logger.warning(
            f"Missing required fields: {', '.join(missing_fields)}"
        )

        return jsonify({
            "error": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    logger.info(f"Creating student: {data.get('email')}")

    student = Student(
        name=data["name"],
        age=data["age"],
        email=data["email"]
    )
    try:
        db.session.add(student)
        db.session.commit()

        logger.info(f"Student created successfully with ID {student.id}")

        return jsonify(student.to_dict()), 201
    except IntegrityError as e:
        # Rollback the session on integrity errors (e.g., duplicate email)
        db.session.rollback()
        logger.warning(
            f"Duplicate email attempted: {data['email']}. Error: {str(e)}"
        )
        return jsonify({
            "error": "Email already exists"
        }), 409
    except Exception as e:
        # Ensure any other errors also rollback and return a 500
        db.session.rollback()
        logger.exception(f"Unexpected error creating student: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500




# GET all students
@student_bp.route("", methods=["GET"])
def get_students():
    logger.info("Fetching all students")
    students = Student.query.all()

    return jsonify(
        [
            student.to_dict()
            for student in students
        ]
    ), 200



# GET student by ID
@student_bp.route("/<int:id>", methods=["GET"])
def get_student(id):
    logger.info(f"Fetching student with ID {id}")

    student = Student.query.get_or_404(id)

    return jsonify(
        student.to_dict()
    ), 200



# UPDATE student
@student_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):
    logger.info(f"Updating student with ID {id}")

    student = Student.query.get_or_404(id)

    data = request.get_json(silent=True)
    if data is None:
        logger.warning(f"Update request for student {id} with empty or invalid JSON")
        return jsonify({"error": "Request body is required and must be in JSON format"}), 400

    allowed_fields = ["name", "age", "email"]
    if not any(field in data for field in allowed_fields):
        logger.warning(f"Update request for student {id} contains no updatable fields")
        return jsonify({"error": "At least one field (name, age, email) must be provided"}), 400

    # Apply updates
    if "name" in data:
        student.name = data["name"]
    if "age" in data:
        student.age = data["age"]
    if "email" in data:
        student.email = data["email"]

    try:
        db.session.commit()
        logger.info(f"Student {id} updated successfully")
        return jsonify(student.to_dict()), 200
    except IntegrityError as e:
        db.session.rollback()
        logger.warning(f"Duplicate email attempted for student {id}: {data.get('email')}. Error: {str(e)}")
        return jsonify({"error": "Email already exists"}), 409
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Unexpected error updating student {id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500



# DELETE student
@student_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):

    student = Student.query.get_or_404(id)
    logger.info(f"Deleting student with ID {id}")

    try:
        db.session.delete(student)
        db.session.commit()
        logger.info(f"Student {id} deleted successfully")

        return jsonify({
            "message": "Student deleted successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Unexpected error deleting student {id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500