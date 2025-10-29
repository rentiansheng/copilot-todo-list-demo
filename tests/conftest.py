from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_es_client():
    """Mock Elasticsearch client for testing"""
    mock_client = MagicMock()
    mock_client.indices.exists.return_value = True
    mock_client.indices.create.return_value = {"acknowledged": True}
    return mock_client


@pytest.fixture
def sample_tree_node():
    """Sample tree node data for testing"""
    return {
        "bk_inst_id": 1,
        "bk_inst_name": "Test Node",
        "cw_status": 1,
        "cw__relation": [],
    }


@pytest.fixture
def sample_tree_node_with_parent():
    """Sample tree node with parent relation"""
    return {
        "bk_inst_id": 2,
        "bk_inst_name": "Child Node",
        "cw_status": 1,
        "cw__relation": [
            {"type": 2, "bk_asst_obj_id": "parent_type", "bk_asst_inst_id": 1}
        ],
    }
