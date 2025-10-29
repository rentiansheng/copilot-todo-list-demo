from fastapi import APIRouter, Body, HTTPException, Path

from app.models.schemas import (
    ServiceBindRequest,
    ServiceUnbindRequest,
    TreeCopyRequest,
    TreeCreateRequest,
    TreeListRequest,
    TreeMoveRequest,
    TreeUpdateRequest,
)
from app.services.tree_service import tree_service

router = APIRouter()


@router.post("/{tree_type}")
async def create_tree(
    tree_type: str = Path(..., description="Type of tree"),
    request: TreeCreateRequest = Body(...),
):
    """Create a new tree node"""
    try:
        result = tree_service.create_tree_node(tree_type, request)
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{tree_type}")
async def update_tree(
    tree_type: str = Path(..., description="Type of tree"),
    request: TreeUpdateRequest = Body(...),
):
    """Update an existing tree node"""
    try:
        result = tree_service.update_tree_node(tree_type, request)
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{tree_type}")
async def delete_tree(
    tree_type: str = Path(..., description="Type of tree"),
    bk_obj_id: str = Body(...),
    bk_inst_id: int = Body(...),
):
    """Delete a tree node (soft delete by setting cw_status to 20)"""
    try:
        result = tree_service.delete_tree_node(tree_type, bk_obj_id, bk_inst_id)
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{tree_type}/move")
async def move_tree(
    tree_type: str = Path(..., description="Type of tree"),
    request: TreeMoveRequest = Body(...),
):
    """Move a tree node to a new parent"""
    try:
        result = tree_service.move_tree_node(tree_type, request)
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{tree_type}/copy")
async def copy_tree(
    tree_type: str = Path(..., description="Type of tree"),
    request: TreeCopyRequest = Body(...),
):
    """Copy a tree node to a new location"""
    try:
        result = tree_service.copy_tree_node(tree_type, request)
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{tree_id}/{parent_obj_id}/{parent_inst_id}/list")
async def list_trees(
    tree_id: str = Path(..., description="Tree ID / bk_obj_id"),
    parent_obj_id: str = Path(..., description="Parent object ID"),
    parent_inst_id: int = Path(..., description="Parent instance ID"),
    request: TreeListRequest = Body(...),
):
    """List tree nodes under a specific parent"""
    try:
        result = tree_service.list_tree_nodes(
            tree_id,
            parent_obj_id,
            parent_inst_id,
            request.page,
            request.page_size,
            request.filters,
        )
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/service/inst/bind")
async def bind_service_instance(request: ServiceBindRequest = Body(...)):
    """Bind a service instance to a tree node"""
    try:
        result = tree_service.bind_service_instance(
            request.service_inst_id, request.bk_inst_id, request.bk_obj_id
        )
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/service/inst/unbind")
async def unbind_service_instance(request: ServiceUnbindRequest = Body(...)):
    """Unbind a service instance from a tree node"""
    try:
        result = tree_service.unbind_service_instance(
            request.service_inst_id, request.bk_inst_id, request.bk_obj_id
        )
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
