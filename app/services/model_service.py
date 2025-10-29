from app.services.elasticsearch import es_service
from app.services.query_builder import IndexMappingBuilder, ESQueryBuilder
from app.models.schemas import TreeObjectCreateRequest
from typing import Dict, List

class ModelService:
    def __init__(self):
        # Use a special index for object models
        self.model_index = "cwcc-object-models"
    
    def create_tree_object(self, request: TreeObjectCreateRequest) -> Dict:
        """Create a tree object model"""
        # Ensure the model index exists
        if not es_service.client.indices.exists(index=self.model_index):
            mapping = IndexMappingBuilder.build_object_model_mapping()
            es_service.client.indices.create(index=self.model_index, body=mapping)
        
        # Create the object model document
        doc = {
            "bk_obj_id": request.bk_obj_id,
            "bk_obj_name": request.bk_obj_name,
            "properties": request.properties or {}
        }
        
        es_service.client.index(index=self.model_index, id=request.bk_obj_id, document=doc)
        
        return doc
    
    def list_tree_objects(self, page: int = 1, page_size: int = 20) -> Dict:
        """List all tree object models"""
        from_index = (page - 1) * page_size
        
        try:
            query = ESQueryBuilder.match_all()
            result = es_service.client.search(
                index=self.model_index,
                body=query,
                from_=from_index,
                size=page_size
            )
            
            items = [hit["_source"] for hit in result["hits"]["hits"]]
            total = result["hits"]["total"]["value"]
            
            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        except:
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size
            }

model_service = ModelService()
