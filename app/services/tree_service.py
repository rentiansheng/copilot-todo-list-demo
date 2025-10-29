from typing import List, Dict, Any, Optional
from app.core.elasticsearch import es_client
from app.models.schemas import (
    TreeNode, TreeNodeCreate, TreeNodeUpdate, TreeNodeMove, TreeNodeCopy,
    TreeNodeList, CWStatus, Relation, RelationType, InstAsst
)

class TreeService:
    def __init__(self):
        self.es = es_client.get_client()
    
    def _get_index_name(self, bk_obj_id: str) -> str:
        """Get index name for object type"""
        return f"cwcc-{bk_obj_id}"
    
    def _generate_inst_id(self, bk_obj_id: str) -> int:
        """Generate new instance ID"""
        index_name = self._get_index_name(bk_obj_id)
        es_client.create_index_with_mapping(bk_obj_id)
        
        # Get max inst_id
        try:
            result = self.es.search(
                index=index_name,
                body={
                    "size": 0,
                    "aggs": {
                        "max_id": {
                            "max": {
                                "field": "bk_inst_id"
                            }
                        }
                    }
                }
            )
            max_id = result['aggregations']['max_id']['value']
            return int(max_id) + 1 if max_id else 1
        except Exception:
            return 1
    
    def create(self, node_data: TreeNodeCreate) -> Dict[str, Any]:
        """Create a new tree node"""
        index_name = self._get_index_name(node_data.bk_obj_id)
        es_client.create_index_with_mapping(node_data.bk_obj_id)
        
        # Generate new instance ID
        bk_inst_id = self._generate_inst_id(node_data.bk_obj_id)
        
        # Build document
        doc = {
            "bk_inst_id": bk_inst_id,
            "bk_inst_name": node_data.bk_inst_name,
            "cw_status": CWStatus.RUNNING,
            "cw__relation": []
        }
        
        # Add properties
        if node_data.properties:
            doc.update(node_data.properties)
        
        # Add parent relation if specified
        if node_data.parent_obj_id and node_data.parent_inst_id:
            relation = {
                "type": RelationType.RELATION,
                "bk_asst_obj_id": node_data.parent_obj_id,
                "bk_asst_inst_id": node_data.parent_inst_id
            }
            doc["cw__relation"].append(relation)
        
        # Index document
        result = self.es.index(index=index_name, id=str(bk_inst_id), document=doc)
        
        return {
            "bk_inst_id": bk_inst_id,
            "bk_obj_id": node_data.bk_obj_id,
            "result": result['result']
        }
    
    def update(self, node_data: TreeNodeUpdate) -> Dict[str, Any]:
        """Update an existing tree node"""
        index_name = self._get_index_name(node_data.bk_obj_id)
        
        # Build update document
        doc = {}
        if node_data.bk_inst_name:
            doc["bk_inst_name"] = node_data.bk_inst_name
        if node_data.cw_status:
            doc["cw_status"] = node_data.cw_status
        if node_data.properties:
            doc.update(node_data.properties)
        
        # Update document
        result = self.es.update(
            index=index_name,
            id=str(node_data.bk_inst_id),
            doc=doc
        )
        
        return {
            "bk_inst_id": node_data.bk_inst_id,
            "bk_obj_id": node_data.bk_obj_id,
            "result": result['result']
        }
    
    def delete(self, bk_obj_id: str, bk_inst_id: int) -> Dict[str, Any]:
        """Delete a tree node (soft delete by setting cw_status to DELETE)"""
        index_name = self._get_index_name(bk_obj_id)
        
        # Soft delete
        result = self.es.update(
            index=index_name,
            id=str(bk_inst_id),
            doc={"cw_status": CWStatus.DELETE}
        )
        
        return {
            "bk_inst_id": bk_inst_id,
            "bk_obj_id": bk_obj_id,
            "result": result['result']
        }
    
    def move(self, move_data: TreeNodeMove) -> Dict[str, Any]:
        """Move a tree node to a new parent"""
        index_name = self._get_index_name(move_data.bk_obj_id)
        
        # Get current document
        doc = self.es.get(index=index_name, id=str(move_data.bk_inst_id))
        current_relations = doc['_source'].get('cw__relation', [])
        
        # Remove old parent relation (type=2)
        new_relations = [r for r in current_relations if r.get('type') != RelationType.RELATION]
        
        # Add new parent relation
        new_relation = {
            "type": RelationType.RELATION,
            "bk_asst_obj_id": move_data.target_parent_obj_id,
            "bk_asst_inst_id": move_data.target_parent_inst_id
        }
        new_relations.append(new_relation)
        
        # Update document
        result = self.es.update(
            index=index_name,
            id=str(move_data.bk_inst_id),
            doc={"cw__relation": new_relations}
        )
        
        return {
            "bk_inst_id": move_data.bk_inst_id,
            "bk_obj_id": move_data.bk_obj_id,
            "result": result['result']
        }
    
    def copy(self, copy_data: TreeNodeCopy) -> Dict[str, Any]:
        """Copy a tree node to a new location"""
        index_name = self._get_index_name(copy_data.bk_obj_id)
        
        # Get source document
        source_doc = self.es.get(index=index_name, id=str(copy_data.bk_inst_id))
        source_data = source_doc['_source']
        
        # Generate new instance ID
        new_inst_id = self._generate_inst_id(copy_data.bk_obj_id)
        
        # Build new document
        new_doc = source_data.copy()
        new_doc['bk_inst_id'] = new_inst_id
        if copy_data.new_inst_name:
            new_doc['bk_inst_name'] = copy_data.new_inst_name
        
        # Update relation to new parent
        new_relations = [r for r in new_doc.get('cw__relation', []) if r.get('type') != RelationType.RELATION]
        new_relation = {
            "type": RelationType.RELATION,
            "bk_asst_obj_id": copy_data.target_parent_obj_id,
            "bk_asst_inst_id": copy_data.target_parent_inst_id
        }
        new_relations.append(new_relation)
        new_doc['cw__relation'] = new_relations
        
        # Index new document
        result = self.es.index(index=index_name, id=str(new_inst_id), document=new_doc)
        
        return {
            "bk_inst_id": new_inst_id,
            "bk_obj_id": copy_data.bk_obj_id,
            "source_inst_id": copy_data.bk_inst_id,
            "result": result['result']
        }
    
    def list_children(
        self, 
        tree_id: str, 
        parent_obj_id: str, 
        parent_inst_id: int, 
        list_data: TreeNodeList
    ) -> Dict[str, Any]:
        """List child nodes under a parent"""
        index_name = self._get_index_name(tree_id)
        
        # Build query
        query = {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "cw__relation",
                            "query": {
                                "bool": {
                                    "must": [
                                        {"term": {"cw__relation.type": RelationType.RELATION}},
                                        {"term": {"cw__relation.bk_asst_obj_id": parent_obj_id}},
                                        {"term": {"cw__relation.bk_asst_inst_id": parent_inst_id}}
                                    ]
                                }
                            }
                        }
                    },
                    {"range": {"cw_status": {"lt": CWStatus.DELETE}}}
                ]
            }
        }
        
        # Add additional filters if provided
        if list_data.filter:
            for key, value in list_data.filter.items():
                query["bool"]["must"].append({"term": {key: value}})
        
        # Calculate pagination
        from_index = (list_data.page - 1) * list_data.page_size
        
        # Search
        try:
            result = self.es.search(
                index=index_name,
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
            logging.error(f"Error listing children for {tree_id}: {e}")
            return {
                "items": [],
                "total": 0,
                "page": list_data.page,
                "page_size": list_data.page_size,
                "error": "Failed to retrieve data"
            }

tree_service = TreeService()
