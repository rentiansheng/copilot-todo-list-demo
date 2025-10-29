from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
from app.models.schemas import TreeObjectCreate, TreeObjectList
from app.services.model_service import model_service

router = APIRouter()

@router.post("/tree/object", summary="Create tree object model")
async def create_tree_object(obj_data: TreeObjectCreate = Body(...)) -> Dict[str, Any]:
    """Create a new tree object model"""
    try:
        result = model_service.create_object(obj_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tree/object/list", summary="List tree object models")
async def list_tree_objects(list_data: TreeObjectList = Body(...)) -> Dict[str, Any]:
    """List all tree object models"""
    try:
        result = model_service.list_objects(list_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
