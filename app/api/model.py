from fastapi import APIRouter, HTTPException, Body
from app.models.schemas import TreeObjectCreateRequest, TreeObjectListRequest
from app.services.model_service import model_service

router = APIRouter()

@router.post("/tree/object")
async def create_tree_object(request: TreeObjectCreateRequest = Body(...)):
    """Create a tree object model"""
    try:
        result = model_service.create_tree_object(request)
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tree/object/list")
async def list_tree_objects(request: TreeObjectListRequest = Body(...)):
    """List all tree object models"""
    try:
        result = model_service.list_tree_objects(request.page, request.page_size)
        return {"code": 0, "data": result, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
