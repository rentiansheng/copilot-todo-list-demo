from typing import Dict, Any
from app.core.elasticsearch import es_client
from app.models.schemas import ServiceInstBind, ServiceInstUnbind, RelationType, InstAsst

class ServiceBindService:
    def __init__(self):
        self.es = es_client.get_client()
    
    def _get_index_name(self, bk_obj_id: str) -> str:
        """Get index name for object type"""
        return f"cwcc-{bk_obj_id}"
    
    def bind(self, bind_data: ServiceInstBind) -> Dict[str, Any]:
        """Bind service instance to target instance"""
        index_name = self._get_index_name(bind_data.service_obj_id)
        
        # Get current document
        doc = self.es.get(index=index_name, id=str(bind_data.service_inst_id))
        current_relations = doc['_source'].get('cw__relation', [])
        
        # Add new binding relation
        new_relation = {
            "type": RelationType.CMDB_INST_ASST,
            "bk_asst_obj_id": bind_data.target_obj_id,
            "bk_asst_inst_id": bind_data.target_inst_id,
            "inst_asst": {
                "bk_obj_asst_id": f"{bind_data.service_obj_id}_{bind_data.target_obj_id}",
                "bk_asst_id": "bind"
            }
        }
        current_relations.append(new_relation)
        
        # Update document
        result = self.es.update(
            index=index_name,
            id=str(bind_data.service_inst_id),
            doc={"cw__relation": current_relations}
        )
        
        return {
            "service_inst_id": bind_data.service_inst_id,
            "target_inst_id": bind_data.target_inst_id,
            "result": result['result']
        }
    
    def unbind(self, unbind_data: ServiceInstUnbind) -> Dict[str, Any]:
        """Unbind service instance from target instance"""
        index_name = self._get_index_name(unbind_data.service_obj_id)
        
        # Get current document
        doc = self.es.get(index=index_name, id=str(unbind_data.service_inst_id))
        current_relations = doc['_source'].get('cw__relation', [])
        
        # Remove binding relation
        new_relations = [
            r for r in current_relations
            if not (
                r.get('type') == RelationType.CMDB_INST_ASST and
                r.get('bk_asst_obj_id') == unbind_data.target_obj_id and
                r.get('bk_asst_inst_id') == unbind_data.target_inst_id
            )
        ]
        
        # Update document
        result = self.es.update(
            index=index_name,
            id=str(unbind_data.service_inst_id),
            doc={"cw__relation": new_relations}
        )
        
        return {
            "service_inst_id": unbind_data.service_inst_id,
            "target_inst_id": unbind_data.target_inst_id,
            "result": result['result']
        }

service_bind_service = ServiceBindService()
