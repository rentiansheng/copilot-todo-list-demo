from elasticsearch import Elasticsearch
from app.config import config
from typing import Optional, List, Dict, Any

class ElasticsearchService:
    def __init__(self):
        self.client = Elasticsearch(
            [config.ELASTICSEARCH_URL],
            basic_auth=(config.ELASTICSEARCH_USER, config.ELASTICSEARCH_PASSWORD)
        )
    
    def get_index_name(self, bk_obj_id: str) -> str:
        """Generate index name based on bk_obj_id"""
        return f"cwcc-{bk_obj_id}"
    
    def create_index_if_not_exists(self, bk_obj_id: str):
        """Create index with proper mapping for nested cw__relation field"""
        index_name = self.get_index_name(bk_obj_id)
        
        if not self.client.indices.exists(index=index_name):
            mapping = {
                "mappings": {
                    "properties": {
                        "bk_inst_id": {"type": "integer"},
                        "bk_inst_name": {"type": "keyword"},
                        "cw_status": {"type": "integer"},
                        "cw__relation": {
                            "type": "nested",
                            "properties": {
                                "type": {"type": "integer"},
                                "inst_asst": {
                                    "properties": {
                                        "bk_obj_asst_id": {"type": "keyword"},
                                        "bk_asst_id": {"type": "keyword"}
                                    }
                                },
                                "bk_asst_obj_id": {"type": "keyword"},
                                "bk_asst_inst_id": {"type": "keyword"}
                            }
                        }
                    }
                }
            }
            self.client.indices.create(index=index_name, body=mapping)
    
    def index_document(self, bk_obj_id: str, doc_id: int, document: Dict[str, Any]) -> Dict:
        """Index a document"""
        self.create_index_if_not_exists(bk_obj_id)
        index_name = self.get_index_name(bk_obj_id)
        return self.client.index(index=index_name, id=doc_id, document=document)
    
    def get_document(self, bk_obj_id: str, doc_id: int) -> Optional[Dict]:
        """Get a document by ID"""
        index_name = self.get_index_name(bk_obj_id)
        try:
            result = self.client.get(index=index_name, id=doc_id)
            return result['_source']
        except:
            return None
    
    def update_document(self, bk_obj_id: str, doc_id: int, document: Dict[str, Any]) -> Dict:
        """Update a document"""
        index_name = self.get_index_name(bk_obj_id)
        return self.client.update(index=index_name, id=doc_id, doc=document)
    
    def delete_document(self, bk_obj_id: str, doc_id: int) -> Dict:
        """Delete a document"""
        index_name = self.get_index_name(bk_obj_id)
        return self.client.delete(index=index_name, id=doc_id)
    
    def search_documents(self, bk_obj_id: str, query: Dict[str, Any], 
                        page: int = 1, page_size: int = 20) -> Dict:
        """Search documents with pagination"""
        index_name = self.get_index_name(bk_obj_id)
        from_index = (page - 1) * page_size
        
        try:
            result = self.client.search(
                index=index_name,
                body=query,
                from_=from_index,
                size=page_size
            )
            return result
        except:
            return {"hits": {"hits": [], "total": {"value": 0}}}
    
    def get_next_id(self, bk_obj_id: str) -> int:
        """Get next available ID for a new document"""
        index_name = self.get_index_name(bk_obj_id)
        try:
            result = self.client.search(
                index=index_name,
                body={
                    "size": 1,
                    "sort": [{"bk_inst_id": {"order": "desc"}}]
                }
            )
            if result['hits']['hits']:
                return result['hits']['hits'][0]['_source']['bk_inst_id'] + 1
            return 1
        except:
            return 1

es_service = ElasticsearchService()
