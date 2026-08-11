from fastapi.testclient import TestClient

from app.main import create_app


def test_health_returns_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_app_initializes_without_feature_modules() -> None:
    app = create_app()

    route_paths = {route.path for route in app.routes}

    assert "/health" in route_paths
    assert "/ready" in route_paths
