from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import IntEnum

class CWStatus(IntEnum):
    """Data lifecycle status"""
    ADD = 1
    RUNNING = 10
    PAUSED = 11
    RUN = 12
    DELETE = 20

class RelationType(IntEnum):
    """Relation type"""
    CMDB_INST_ASST = 1  # CMDB instance association
    RELATION = 2  # Parent-child relation

class InstAsst(BaseModel):
    """Instance association"""
    bk_obj_asst_id: str
    bk_asst_id: str

class Relation(BaseModel):
    """Relation structure"""
    type: RelationType
    inst_asst: Optional[InstAsst] = None
    bk_asst_obj_id: str
    bk_asst_inst_id: int

class TreeNode(BaseModel):
    """Tree node data structure stored in ES"""
    bk_inst_id: int
    bk_inst_name: str
    cw_status: CWStatus = CWStatus.RUNNING
    cw__relation: List[Relation] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True

class TreeNodeCreate(BaseModel):
    """Create tree node request"""
    bk_obj_id: str
    bk_inst_name: str
    parent_obj_id: Optional[str] = None
    parent_inst_id: Optional[int] = None
    properties: Optional[Dict[str, Any]] = None

class TreeNodeUpdate(BaseModel):
    """Update tree node request"""
    bk_obj_id: str
    bk_inst_id: int
    bk_inst_name: Optional[str] = None
    cw_status: Optional[CWStatus] = None
    properties: Optional[Dict[str, Any]] = None

class TreeNodeMove(BaseModel):
    """Move tree node request"""
    bk_obj_id: str
    bk_inst_id: int
    target_parent_obj_id: str
    target_parent_inst_id: int

class TreeNodeCopy(BaseModel):
    """Copy tree node request"""
    bk_obj_id: str
    bk_inst_id: int
    target_parent_obj_id: str
    target_parent_inst_id: int
    new_inst_name: Optional[str] = None

class TreeNodeList(BaseModel):
    """List tree nodes request"""
    page: int = 1
    page_size: int = 20
    filter: Optional[Dict[str, Any]] = None

class ServiceInstBind(BaseModel):
    """Service instance bind request"""
    service_obj_id: str
    service_inst_id: int
    target_obj_id: str
    target_inst_id: int

class ServiceInstUnbind(BaseModel):
    """Service instance unbind request"""
    service_obj_id: str
    service_inst_id: int
    target_obj_id: str
    target_inst_id: int

class TreeObjectCreate(BaseModel):
    """Tree object model create request"""
    bk_obj_id: str
    bk_obj_name: str
    properties: Optional[Dict[str, Any]] = None

class TreeObjectList(BaseModel):
    """Tree object model list request"""
    page: int = 1
    page_size: int = 20
    filter: Optional[Dict[str, Any]] = None
