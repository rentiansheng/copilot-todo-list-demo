import pytest
from pydantic import ValidationError

from app.models.schemas import (
    InstAsst,
    Relation,
    ServiceBindRequest,
    ServiceUnbindRequest,
    TreeCopyRequest,
    TreeCreateRequest,
    TreeListRequest,
    TreeMoveRequest,
    TreeNode,
    TreeObjectCreateRequest,
    TreeObjectListRequest,
    TreeUpdateRequest,
)


class TestInstAsst:
    """Test InstAsst model"""

    def test_valid_inst_asst(self):
        """Test creating valid InstAsst"""
        inst_asst = InstAsst(bk_obj_asst_id="asst_1", bk_asst_id="id_1")
        assert inst_asst.bk_obj_asst_id == "asst_1"
        assert inst_asst.bk_asst_id == "id_1"


class TestRelation:
    """Test Relation model"""

    def test_relation_type_1(self):
        """Test relation with type 1"""
        relation = Relation(
            type=1,
            bk_asst_obj_id="obj_1",
            bk_asst_inst_id="inst_1",
            inst_asst=InstAsst(bk_obj_asst_id="asst_1", bk_asst_id="id_1"),
        )
        assert relation.type == 1
        assert relation.inst_asst is not None

    def test_relation_type_2(self):
        """Test relation with type 2"""
        relation = Relation(type=2, bk_asst_obj_id="obj_1", bk_asst_inst_id=123)
        assert relation.type == 2
        assert relation.inst_asst is None

    def test_relation_invalid_type(self):
        """Test relation with invalid type"""
        with pytest.raises(ValidationError):
            Relation(type=3, bk_asst_obj_id="obj_1", bk_asst_inst_id="inst_1")


class TestTreeNode:
    """Test TreeNode model"""

    def test_valid_tree_node(self):
        """Test creating valid tree node"""
        node = TreeNode(
            bk_inst_id=1,
            bk_inst_name="Test Node",
            cw_status=1,
            cw__relation=[],
        )
        assert node.bk_inst_id == 1
        assert node.bk_inst_name == "Test Node"
        assert node.cw_status == 1
        assert node.cw__relation == []

    def test_tree_node_with_relations(self):
        """Test tree node with relations"""
        relation = Relation(type=2, bk_asst_obj_id="parent", bk_asst_inst_id=1)
        node = TreeNode(
            bk_inst_id=2,
            bk_inst_name="Child Node",
            cw_status=10,
            cw__relation=[relation],
        )
        assert len(node.cw__relation) == 1
        assert node.cw__relation[0].type == 2

    def test_tree_node_invalid_status(self):
        """Test tree node with invalid status"""
        with pytest.raises(ValidationError):
            TreeNode(
                bk_inst_id=1,
                bk_inst_name="Test",
                cw_status=99,  # Invalid status
            )

    def test_tree_node_allows_extra_fields(self):
        """Test tree node allows additional fields"""
        node = TreeNode(
            bk_inst_id=1,
            bk_inst_name="Test",
            cw_status=1,
            custom_field="custom_value",
        )
        assert hasattr(node, "custom_field")


class TestTreeCreateRequest:
    """Test TreeCreateRequest model"""

    def test_minimal_create_request(self):
        """Test minimal create request"""
        req = TreeCreateRequest(bk_inst_name="New Node", bk_obj_id="server")
        assert req.bk_inst_name == "New Node"
        assert req.bk_obj_id == "server"
        assert req.parent_obj_id is None
        assert req.parent_inst_id is None

    def test_create_request_with_parent(self):
        """Test create request with parent"""
        req = TreeCreateRequest(
            bk_inst_name="Child",
            bk_obj_id="server",
            parent_obj_id="rack",
            parent_inst_id=1,
        )
        assert req.parent_obj_id == "rack"
        assert req.parent_inst_id == 1


class TestTreeUpdateRequest:
    """Test TreeUpdateRequest model"""

    def test_update_request(self):
        """Test update request"""
        req = TreeUpdateRequest(
            bk_inst_id=1, bk_obj_id="server", bk_inst_name="Updated", cw_status=10
        )
        assert req.bk_inst_id == 1
        assert req.bk_inst_name == "Updated"
        assert req.cw_status == 10


class TestTreeMoveRequest:
    """Test TreeMoveRequest model"""

    def test_move_request(self):
        """Test move request"""
        req = TreeMoveRequest(
            bk_inst_id=1,
            bk_obj_id="server",
            target_parent_obj_id="rack",
            target_parent_inst_id=2,
        )
        assert req.target_parent_obj_id == "rack"
        assert req.target_parent_inst_id == 2


class TestTreeCopyRequest:
    """Test TreeCopyRequest model"""

    def test_copy_request(self):
        """Test copy request"""
        req = TreeCopyRequest(
            bk_inst_id=1,
            bk_obj_id="server",
            target_parent_obj_id="rack",
            target_parent_inst_id=2,
            new_inst_name="Copy of Server",
        )
        assert req.new_inst_name == "Copy of Server"

    def test_copy_request_no_name(self):
        """Test copy request without new name"""
        req = TreeCopyRequest(
            bk_inst_id=1,
            bk_obj_id="server",
            target_parent_obj_id="rack",
            target_parent_inst_id=2,
        )
        assert req.new_inst_name is None


class TestTreeListRequest:
    """Test TreeListRequest model"""

    def test_list_request_defaults(self):
        """Test list request with defaults"""
        req = TreeListRequest()
        assert req.page == 1
        assert req.page_size == 20
        assert req.filters is None

    def test_list_request_custom(self):
        """Test list request with custom values"""
        req = TreeListRequest(page=2, page_size=50, filters={"status": 10})
        assert req.page == 2
        assert req.page_size == 50
        assert req.filters == {"status": 10}


class TestServiceBindRequest:
    """Test ServiceBindRequest model"""

    def test_bind_request(self):
        """Test bind request"""
        req = ServiceBindRequest(service_inst_id=100, bk_inst_id=1, bk_obj_id="server")
        assert req.service_inst_id == 100
        assert req.bk_inst_id == 1


class TestServiceUnbindRequest:
    """Test ServiceUnbindRequest model"""

    def test_unbind_request(self):
        """Test unbind request"""
        req = ServiceUnbindRequest(
            service_inst_id=100, bk_inst_id=1, bk_obj_id="server"
        )
        assert req.service_inst_id == 100


class TestTreeObjectCreateRequest:
    """Test TreeObjectCreateRequest model"""

    def test_object_create_request(self):
        """Test object create request"""
        req = TreeObjectCreateRequest(
            bk_obj_id="server", bk_obj_name="Server", properties={"cpu": "string"}
        )
        assert req.bk_obj_id == "server"
        assert req.bk_obj_name == "Server"
        assert req.properties == {"cpu": "string"}


class TestTreeObjectListRequest:
    """Test TreeObjectListRequest model"""

    def test_object_list_request(self):
        """Test object list request"""
        req = TreeObjectListRequest(page=1, page_size=20)
        assert req.page == 1
        assert req.page_size == 20
