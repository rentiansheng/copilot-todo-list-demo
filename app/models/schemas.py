from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class InstAsst(BaseModel):
    """Instance association info"""

    bk_obj_asst_id: str
    bk_asst_id: str


class Relation(BaseModel):
    """Relation structure for cw__relation field"""

    type: Literal[1, 2]  # 1: cmdb inst asst, 2: relation
    inst_asst: Optional[InstAsst] = None
    bk_asst_obj_id: str
    bk_asst_inst_id: Union[str, int]


class TreeNode(BaseModel):
    """Tree node data structure as per README"""

    bk_inst_id: int
    bk_inst_name: str
    cw_status: Literal[
        1, 10, 11, 12, 20
    ] = 1  # 1: add, 10: running, 11: paused, 12: run, 20: delete
    cw__relation: List[Relation] = Field(default_factory=list)

    class Config:
        extra = "allow"  # Allow additional fields


class TreeCreateRequest(BaseModel):
    """Request model for creating a tree node"""

    bk_inst_name: str
    bk_obj_id: str
    parent_obj_id: Optional[str] = None
    parent_inst_id: Optional[int] = None
    additional_fields: Optional[dict] = None


class TreeUpdateRequest(BaseModel):
    """Request model for updating a tree node"""

    bk_inst_id: int
    bk_obj_id: str
    bk_inst_name: Optional[str] = None
    cw_status: Optional[Literal[1, 10, 11, 12, 20]] = None
    additional_fields: Optional[dict] = None


class TreeMoveRequest(BaseModel):
    """Request model for moving a tree node"""

    bk_inst_id: int
    bk_obj_id: str
    target_parent_obj_id: str
    target_parent_inst_id: int


class TreeCopyRequest(BaseModel):
    """Request model for copying a tree node"""

    bk_inst_id: int
    bk_obj_id: str
    target_parent_obj_id: str
    target_parent_inst_id: int
    new_inst_name: Optional[str] = None


class TreeListRequest(BaseModel):
    """Request model for listing tree nodes"""

    page: int = 1
    page_size: int = 20
    filters: Optional[dict] = None


class ServiceBindRequest(BaseModel):
    """Request model for service instance binding"""

    service_inst_id: int
    bk_inst_id: int
    bk_obj_id: str


class ServiceUnbindRequest(BaseModel):
    """Request model for service instance unbinding"""

    service_inst_id: int
    bk_inst_id: int
    bk_obj_id: str


class TreeObjectCreateRequest(BaseModel):
    """Request model for creating tree object model"""

    bk_obj_id: str
    bk_obj_name: str
    properties: Optional[dict] = None


class TreeObjectListRequest(BaseModel):
    """Request model for listing tree object models"""

    page: int = 1
    page_size: int = 20
