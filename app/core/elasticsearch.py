from elasticsearch import Elasticsearch
from typing import Optional
from app.core.config import settings

class ElasticsearchClient:
    _instance = None
    _client: Optional[Elasticsearch] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_client(self) -> Elasticsearch:
        """Get or create Elasticsearch client"""
        if self._client is None:
            # Add scheme if not present
            host = settings.elasticsearch_host
            if not host.startswith(('http://', 'https://')):
                host = f'http://{host}'
            self._client = Elasticsearch(
                [host],
                basic_auth=(settings.elasticsearch_user, settings.elasticsearch_password)
            )
        return self._client
    
    def create_index_with_mapping(self, bk_obj_id: str):
        """Create ES index with proper mapping for cw__relation nested field"""
        index_name = f"cwcc-{bk_obj_id}"
        
        client = self.get_client()
        if client.indices.exists(index=index_name):
            return index_name
        
        mapping = {
            "mappings": {
                "properties": {
                    "bk_inst_id": {"type": "long"},
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
                            "bk_asst_inst_id": {"type": "long"}
                        }
                    }
                }
            }
        }
        
        client.indices.create(index=index_name, body=mapping)
        return index_name

es_client = ElasticsearchClient()
