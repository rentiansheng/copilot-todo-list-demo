from fastapi import APIRouter, HTTPException, Path, Body
from typing import Dict, Any
from app.models.schemas import (
    TreeNodeCreate, TreeNodeUpdate, TreeNodeMove, TreeNodeCopy, TreeNodeList,
    ServiceInstBind, ServiceInstUnbind
)
from app.services.tree_service import tree_service
from app.services.service_bind_service import service_bind_service

router = APIRouter()

@router.post("/{type}", summary="Create tree node")
async def create_tree_node(
    type: str = Path(..., description="Object type ID"),
    node_data: TreeNodeCreate = Body(...)
) -> Dict[str, Any]:
    """Create a new tree node"""
    try:
        # Override bk_obj_id with path parameter
        node_data.bk_obj_id = type
        result = tree_service.create(node_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{type}", summary="Update tree node")
async def update_tree_node(
    type: str = Path(..., description="Object type ID"),
    node_data: TreeNodeUpdate = Body(...)
) -> Dict[str, Any]:
    """Update an existing tree node"""
    try:
        # Override bk_obj_id with path parameter
        node_data.bk_obj_id = type
        result = tree_service.update(node_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{type}", summary="Delete tree node")
async def delete_tree_node(
    type: str = Path(..., description="Object type ID"),
    bk_inst_id: int = Body(..., embed=True)
) -> Dict[str, Any]:
    """Delete a tree node (soft delete)"""
    try:
        result = tree_service.delete(type, bk_inst_id)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{type}/move", summary="Move tree node")
async def move_tree_node(
    type: str = Path(..., description="Object type ID"),
    move_data: TreeNodeMove = Body(...)
) -> Dict[str, Any]:
    """Move a tree node to a new parent"""
    try:
        # Override bk_obj_id with path parameter
        move_data.bk_obj_id = type
        result = tree_service.move(move_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{type}/copy", summary="Copy tree node")
async def copy_tree_node(
    type: str = Path(..., description="Object type ID"),
    copy_data: TreeNodeCopy = Body(...)
) -> Dict[str, Any]:
    """Copy a tree node to a new location"""
    try:
        # Override bk_obj_id with path parameter
        copy_data.bk_obj_id = type
        result = tree_service.copy(copy_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{tree_id}/{parent_obj_id}/{parent_inst_id}/list", summary="List tree nodes")
async def list_tree_nodes(
    tree_id: str = Path(..., description="Tree/Object type ID"),
    parent_obj_id: str = Path(..., description="Parent object type ID"),
    parent_inst_id: int = Path(..., description="Parent instance ID"),
    list_data: TreeNodeList = Body(...)
) -> Dict[str, Any]:
    """List child nodes under a parent"""
    try:
        result = tree_service.list_children(tree_id, parent_obj_id, parent_inst_id, list_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/service/inst/bind", summary="Bind service instance")
async def bind_service_instance(bind_data: ServiceInstBind = Body(...)) -> Dict[str, Any]:
    """Bind service instance to target instance"""
    try:
        result = service_bind_service.bind(bind_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/service/inst/unbind", summary="Unbind service instance")
async def unbind_service_instance(unbind_data: ServiceInstUnbind = Body(...)) -> Dict[str, Any]:
    """Unbind service instance from target instance"""
    try:
        result = service_bind_service.unbind(unbind_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
