from app.services.elasticsearch import es_service
from app.models.schemas import (
    TreeNode, TreeCreateRequest, TreeUpdateRequest, 
    TreeMoveRequest, TreeCopyRequest, Relation
)
from typing import List, Dict, Any, Optional

class TreeService:
    def create_tree_node(self, tree_type: str, request: TreeCreateRequest) -> TreeNode:
        """Create a new tree node"""
        bk_inst_id = es_service.get_next_id(request.bk_obj_id)
        
        # Build relations if parent is specified
        relations = []
        if request.parent_obj_id and request.parent_inst_id:
            relations.append(Relation(
                type=2,
                bk_asst_obj_id=request.parent_obj_id,
                bk_asst_inst_id=request.parent_inst_id
            ))
        
        # Create document
        doc = {
            "bk_inst_id": bk_inst_id,
            "bk_inst_name": request.bk_inst_name,
            "cw_status": 1,  # add status
            "cw__relation": [r.dict() for r in relations]
        }
        
        # Add additional fields if provided
        if request.additional_fields:
            doc.update(request.additional_fields)
        
        es_service.index_document(request.bk_obj_id, bk_inst_id, doc)
        
        return TreeNode(**doc)
    
    def update_tree_node(self, tree_type: str, request: TreeUpdateRequest) -> TreeNode:
        """Update an existing tree node"""
        # Get existing document
        existing = es_service.get_document(request.bk_obj_id, request.bk_inst_id)
        if not existing:
            raise ValueError(f"Tree node {request.bk_inst_id} not found")
        
        # Update fields
        update_doc = {}
        if request.bk_inst_name:
            update_doc["bk_inst_name"] = request.bk_inst_name
        if request.cw_status is not None:
            update_doc["cw_status"] = request.cw_status
        if request.additional_fields:
            update_doc.update(request.additional_fields)
        
        es_service.update_document(request.bk_obj_id, request.bk_inst_id, update_doc)
        
        # Get updated document
        updated = es_service.get_document(request.bk_obj_id, request.bk_inst_id)
        return TreeNode(**updated)
    
    def delete_tree_node(self, tree_type: str, bk_obj_id: str, bk_inst_id: int) -> Dict:
        """Soft delete a tree node by setting cw_status to 20"""
        existing = es_service.get_document(bk_obj_id, bk_inst_id)
        if not existing:
            raise ValueError(f"Tree node {bk_inst_id} not found")
        
        es_service.update_document(bk_obj_id, bk_inst_id, {"cw_status": 20})
        return {"message": "Tree node deleted successfully"}
    
    def move_tree_node(self, tree_type: str, request: TreeMoveRequest) -> TreeNode:
        """Move a tree node to a new parent"""
        existing = es_service.get_document(request.bk_obj_id, request.bk_inst_id)
        if not existing:
            raise ValueError(f"Tree node {request.bk_inst_id} not found")
        
        # Update relations to reflect new parent
        relations = existing.get("cw__relation", [])
        
        # Remove old parent relation and add new one
        relations = [r for r in relations if r.get("type") != 2]
        relations.append({
            "type": 2,
            "bk_asst_obj_id": request.target_parent_obj_id,
            "bk_asst_inst_id": request.target_parent_inst_id
        })
        
        es_service.update_document(request.bk_obj_id, request.bk_inst_id, 
                                   {"cw__relation": relations})
        
        updated = es_service.get_document(request.bk_obj_id, request.bk_inst_id)
        return TreeNode(**updated)
    
    def copy_tree_node(self, tree_type: str, request: TreeCopyRequest) -> TreeNode:
        """Copy a tree node to a new location"""
        existing = es_service.get_document(request.bk_obj_id, request.bk_inst_id)
        if not existing:
            raise ValueError(f"Tree node {request.bk_inst_id} not found")
        
        # Create new ID for the copy
        new_inst_id = es_service.get_next_id(request.bk_obj_id)
        
        # Create copy with new parent relation
        new_doc = existing.copy()
        new_doc["bk_inst_id"] = new_inst_id
        new_doc["bk_inst_name"] = request.new_inst_name or f"{existing['bk_inst_name']}_copy"
        new_doc["cw_status"] = 1  # New copy starts in 'add' status
        
        # Set parent relation
        new_doc["cw__relation"] = [{
            "type": 2,
            "bk_asst_obj_id": request.target_parent_obj_id,
            "bk_asst_inst_id": request.target_parent_inst_id
        }]
        
        es_service.index_document(request.bk_obj_id, new_inst_id, new_doc)
        
        return TreeNode(**new_doc)
    
    def list_tree_nodes(self, tree_id: str, parent_obj_id: str, 
                       parent_inst_id: int, page: int = 1, 
                       page_size: int = 20, filters: Optional[Dict] = None) -> Dict:
        """List tree nodes under a specific parent"""
        # Build query to find children of the parent
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "nested": {
                                "path": "cw__relation",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {"term": {"cw__relation.type": 2}},
                                            {"term": {"cw__relation.bk_asst_obj_id": parent_obj_id}},
                                            {"term": {"cw__relation.bk_asst_inst_id": str(parent_inst_id)}}
                                        ]
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        
        # Add additional filters if provided
        if filters:
            for key, value in filters.items():
                query["query"]["bool"]["must"].append({"term": {key: value}})
        
        result = es_service.search_documents(tree_id, query, page, page_size)
        
        items = [hit["_source"] for hit in result["hits"]["hits"]]
        total = result["hits"]["total"]["value"]
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    
    def bind_service_instance(self, service_inst_id: int, bk_inst_id: int, 
                             bk_obj_id: str) -> Dict:
        """Bind a service instance to a tree node"""
        existing = es_service.get_document(bk_obj_id, bk_inst_id)
        if not existing:
            raise ValueError(f"Tree node {bk_inst_id} not found")
        
        relations = existing.get("cw__relation", [])
        
        # Add service binding relation
        relations.append({
            "type": 1,
            "bk_asst_obj_id": "service",
            "bk_asst_inst_id": service_inst_id,
            "inst_asst": {
                "bk_obj_asst_id": "service_binding",
                "bk_asst_id": "bind"
            }
        })
        
        es_service.update_document(bk_obj_id, bk_inst_id, {"cw__relation": relations})
        
        return {"message": "Service instance bound successfully"}
    
    def unbind_service_instance(self, service_inst_id: int, bk_inst_id: int, 
                               bk_obj_id: str) -> Dict:
        """Unbind a service instance from a tree node"""
        existing = es_service.get_document(bk_obj_id, bk_inst_id)
        if not existing:
            raise ValueError(f"Tree node {bk_inst_id} not found")
        
        relations = existing.get("cw__relation", [])
        
        # Remove service binding relation
        relations = [
            r for r in relations 
            if not (r.get("type") == 1 and r.get("bk_asst_inst_id") == service_inst_id)
        ]
        
        es_service.update_document(bk_obj_id, bk_inst_id, {"cw__relation": relations})
        
        return {"message": "Service instance unbound successfully"}

tree_service = TreeService()
