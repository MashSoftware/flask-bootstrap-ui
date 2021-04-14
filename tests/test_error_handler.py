from app import create_app


def test_not_found():
    app = create_app()

    with app.test_client() as test_client:
        response = test_client.get("/does-not-exist")
        assert response.status_code == 404
        assert response.mimetype == "text/html"


def test_method_not_allowed():
    app = create_app()

    with app.test_client() as test_client:
        response = test_client.post("/")
        assert response.status_code == 405
        assert response.mimetype == "text/html"
