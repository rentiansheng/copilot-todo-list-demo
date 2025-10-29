from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import TreeNode


@pytest.fixture
def client():
    """Create test client with mocked ES"""
    with patch("app.services.elasticsearch.Elasticsearch"):
        from main import app

        return TestClient(app)


class TestTreeAPI:
    """Test tree API endpoints"""

    def test_create_tree(self, client):
        """Test creating a tree node"""
        with patch("app.api.tree.tree_service") as mock_service:
            mock_service.create_tree_node.return_value = TreeNode(
                bk_inst_id=1,
                bk_inst_name="Test Node",
                cw_status=1,
                cw__relation=[],
            )

            response = client.post(
                "/api/tree/server",
                json={
                    "bk_inst_name": "Test Node",
                    "bk_obj_id": "server",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0
            assert data["message"] == "success"

    def test_update_tree(self, client):
        """Test updating a tree node"""
        with patch("app.api.tree.tree_service") as mock_service:
            mock_service.update_tree_node.return_value = TreeNode(
                bk_inst_id=1,
                bk_inst_name="Updated Node",
                cw_status=10,
                cw__relation=[],
            )

            response = client.put(
                "/api/tree/server",
                json={
                    "bk_inst_id": 1,
                    "bk_obj_id": "server",
                    "bk_inst_name": "Updated Node",
                    "cw_status": 10,
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0

    def test_delete_tree(self, client):
        """Test deleting a tree node"""
        with patch("app.api.tree.tree_service") as mock_service:
            mock_service.delete_tree_node.return_value = {
                "message": "Tree node deleted successfully"
            }

            response = client.request(
                "DELETE",
                "/api/tree/server",
                json={"bk_obj_id": "server", "bk_inst_id": 1},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0

    def test_move_tree(self, client):
        """Test moving a tree node"""
        with patch("app.api.tree.tree_service") as mock_service:
            mock_service.move_tree_node.return_value = TreeNode(
                bk_inst_id=1, bk_inst_name="Node", cw_status=1, cw__relation=[]
            )

            response = client.post(
                "/api/tree/server/move",
                json={
                    "bk_inst_id": 1,
                    "bk_obj_id": "server",
                    "target_parent_obj_id": "rack",
                    "target_parent_inst_id": 2,
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0

    def test_copy_tree(self, client):
        """Test copying a tree node"""
        with patch("app.api.tree.tree_service") as mock_service:
            mock_service.copy_tree_node.return_value = TreeNode(
                bk_inst_id=2,
                bk_inst_name="Node Copy",
                cw_status=1,
                cw__relation=[],
            )

            response = client.post(
                "/api/tree/server/copy",
                json={
                    "bk_inst_id": 1,
                    "bk_obj_id": "server",
                    "target_parent_obj_id": "rack",
                    "target_parent_inst_id": 2,
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0

    def test_list_trees(self, client):
        """Test listing tree nodes"""
        with patch("app.api.tree.tree_service") as mock_service:
            mock_service.list_tree_nodes.return_value = {
                "items": [],
                "total": 0,
                "page": 1,
                "page_size": 20,
            }

            response = client.post(
                "/api/tree/server/server/1/list",
                json={"page": 1, "page_size": 20},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0
            assert "items" in data["data"]

    def test_bind_service(self, client):
        """Test binding service instance"""
        with patch("app.api.tree.tree_service") as mock_service:
            mock_service.bind_service_instance.return_value = {
                "message": "Service instance bound successfully"
            }

            response = client.post(
                "/api/tree/service/inst/bind",
                json={"service_inst_id": 100, "bk_inst_id": 1, "bk_obj_id": "server"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0

    def test_unbind_service(self, client):
        """Test unbinding service instance"""
        with patch("app.api.tree.tree_service") as mock_service:
            mock_service.unbind_service_instance.return_value = {
                "message": "Service instance unbound successfully"
            }

            response = client.post(
                "/api/tree/service/inst/unbind",
                json={"service_inst_id": 100, "bk_inst_id": 1, "bk_obj_id": "server"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 0

    def test_create_tree_error(self, client):
        """Test error handling in create tree"""
        with patch("app.api.tree.tree_service") as mock_service:
            mock_service.create_tree_node.side_effect = ValueError("Test error")

            response = client.post(
                "/api/tree/server",
                json={
                    "bk_inst_name": "Test Node",
                    "bk_obj_id": "server",
                },
            )

            assert response.status_code == 400
