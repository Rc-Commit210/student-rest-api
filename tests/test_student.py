import os
import tempfile

import pytest

from app import create_app
from app.database import db


@pytest.fixture
def client():
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")

        app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            }
        )

        with app.app_context():
            db.create_all()

            with app.test_client() as test_client:
                yield test_client

            db.session.remove()
            db.drop_all()
            db.engine.dispose()


def test_create_student(client):
    response = client.post(
        "/api/v1/students",
        json={
            "name": "Rahul",
            "age": 24,
            "email": "rahul_test@example.com",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Rahul"
    assert data["age"] == 24
    assert data["email"] == "rahul_test@example.com"


def test_get_students(client):
    client.post(
        "/api/v1/students",
        json={
            "name": "Rahul",
            "age": 24,
            "email": "rahul1@example.com",
        },
    )

    client.post(
        "/api/v1/students",
        json={
            "name": "Amit",
            "age": 25,
            "email": "amit1@example.com",
        },
    )

    response = client.get("/api/v1/students")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Rahul"
    assert data[1]["name"] == "Amit"


def test_get_student_by_id(client):
    create_response = client.post(
        "/api/v1/students",
        json={
            "name": "Sanket",
            "age": 25,
            "email": "sanket_test@example.com",
        },
    )

    student = create_response.get_json()
    student_id = student["id"]

    response = client.get(f"/api/v1/students/{student_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == student_id
    assert data["name"] == "Sanket"
    assert data["age"] == 25
    assert data["email"] == "sanket_test@example.com"


def test_update_student(client):
    create_response = client.post(
        "/api/v1/students",
        json={
            "name": "Rahul",
            "age": 24,
            "email": "rahul_update@example.com",
        },
    )

    student = create_response.get_json()
    student_id = student["id"]

    response = client.put(
        f"/api/v1/students/{student_id}",
        json={
            "name": "Rahul Sharma",
            "age": 25,
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == student_id
    assert data["name"] == "Rahul Sharma"
    assert data["age"] == 25
    assert data["email"] == "rahul_update@example.com"


def test_delete_student(client):
    create_response = client.post(
        "/api/v1/students",
        json={
            "name": "Delete Me",
            "age": 30,
            "email": "delete@example.com",
        },
    )

    student = create_response.get_json()
    student_id = student["id"]

    response = client.delete(f"/api/v1/students/{student_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Student deleted successfully"

    response = client.get(f"/api/v1/students/{student_id}")

    assert response.status_code == 404
