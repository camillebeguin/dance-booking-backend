from fastapi.testclient import TestClient


def test_can_create_studio(test_client: TestClient):
    response = test_client.post(
        "/studio",
        json={
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Studio 1",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip_code": "12345",
                "country": "USA",
            },
        },
    )
    assert response.status_code == 201
