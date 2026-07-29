from app import create_app


def test_healthcheck():

    app = create_app()

    app.testing = True

    client = app.test_client()

    response = client.get("/healthcheck")

    assert response.status_code == 200

    assert response.json["status"] == "UP"

    assert response.json["message"] == "Student API is running"