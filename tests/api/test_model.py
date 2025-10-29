from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client with mocked ES"""
    with patch("app.services.elasticsearch.Elasticsearch"):
        from main import app

        return TestClient(app)


class TestModelAPI:
    """Test model API endpoints"""

    def test_create_tree_object(self, client):
        """Test creating a tree object model"""
        with patch("app.api.model.model_service") as mock_service:
            mock_service.create_tree_object.return_value = {
                "bk_obj_id": "server",
                "bk_obj_name": "Server",
                "properties": {},
            }

            response = client.post(
                "/api/model/tree/object",
                json={
                    "bk_obj_id": "server",
                    "bk_obj_name": "Server",
                    "properties": {},
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0
            assert data["message"] == "success"

    def test_list_tree_objects(self, client):
        """Test listing tree object models"""
        with patch("app.api.model.model_service") as mock_service:
            mock_service.list_tree_objects.return_value = {
                "items": [],
                "total": 0,
                "page": 1,
                "page_size": 20,
            }

            response = client.post(
                "/api/model/tree/object/list",
                json={"page": 1, "page_size": 20},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0
            assert "items" in data["data"]

    def test_create_tree_object_error(self, client):
        """Test error handling in create tree object"""
        with patch("app.api.model.model_service") as mock_service:
            mock_service.create_tree_object.side_effect = Exception("Test error")

            response = client.post(
                "/api/model/tree/object",
                json={
                    "bk_obj_id": "server",
                    "bk_obj_name": "Server",
                },
            )

            assert response.status_code == 400
