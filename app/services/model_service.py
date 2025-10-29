from typing import Dict, Any, List
from app.core.elasticsearch import es_client
from app.models.schemas import TreeObjectCreate, TreeObjectList

class ModelService:
    def __init__(self):
        self.es = es_client.get_client()
        self.model_index = "cwcc-tree-models"
    
    def _ensure_model_index(self):
        """Ensure model index exists"""
        if not self.es.indices.exists(index=self.model_index):
            mapping = {
                "mappings": {
                    "properties": {
                        "bk_obj_id": {"type": "keyword"},
                        "bk_obj_name": {"type": "keyword"}
                    }
                }
            }
            self.es.indices.create(index=self.model_index, body=mapping)
    
    def create_object(self, obj_data: TreeObjectCreate) -> Dict[str, Any]:
        """Create a tree object model"""
        self._ensure_model_index()
        
        # Build document
        doc = {
            "bk_obj_id": obj_data.bk_obj_id,
            "bk_obj_name": obj_data.bk_obj_name
        }
        
        # Add properties
        if obj_data.properties:
            doc.update(obj_data.properties)
        
        # Index document
        result = self.es.index(index=self.model_index, id=obj_data.bk_obj_id, document=doc)
        
        # Also create ES index for this object type
        es_client.create_index_with_mapping(obj_data.bk_obj_id)
        
        return {
            "bk_obj_id": obj_data.bk_obj_id,
            "result": result['result']
        }
    
    def list_objects(self, list_data: TreeObjectList) -> Dict[str, Any]:
        """List tree object models"""
        self._ensure_model_index()
        
        # Build query
        query = {"match_all": {}}
        
        # Add filters if provided
        if list_data.filter:
            must_clauses = []
            for key, value in list_data.filter.items():
                must_clauses.append({"term": {key: value}})
            query = {"bool": {"must": must_clauses}}
        
        # Calculate pagination
        from_index = (list_data.page - 1) * list_data.page_size
        
        # Search
        try:
            result = self.es.search(
                index=self.model_index,
                query=query,
                from_=from_index,
                size=list_data.page_size
            )
            
            items = [hit['_source'] for hit in result['hits']['hits']]
            total = result['hits']['total']['value']
            
            return {
                "items": items,
                "total": total,
                "page": list_data.page,
                "page_size": list_data.page_size
            }
        except Exception as e:
            # Log the error but return generic message
            import logging
            logging.error(f"Error listing objects: {e}")
            return {
                "items": [],
                "total": 0,
                "page": list_data.page,
                "page_size": list_data.page_size,
                "error": "Failed to retrieve data"
            }

model_service = ModelService()
