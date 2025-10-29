from typing import Any, Dict, List


class ESQueryBuilder:
    """Builder class for constructing Elasticsearch queries in a maintainable way"""

    @staticmethod
    def match_all() -> Dict[str, Any]:
        """Build a match_all query"""
        return {"query": {"match_all": {}}}

    @staticmethod
    def term(field: str, value: Any) -> Dict[str, Any]:
        """Build a term query for exact matching"""
        return {"term": {field: value}}

    @staticmethod
    def terms(field: str, values: List[Any]) -> Dict[str, Any]:
        """Build a terms query for matching multiple values"""
        return {"terms": {field: values}}

    @staticmethod
    def nested(path: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Build a nested query"""
        return {"nested": {"path": path, "query": query}}

    @staticmethod
    def bool_must(conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build a bool query with must conditions"""
        return {"bool": {"must": conditions}}

    @staticmethod
    def bool_should(
        conditions: List[Dict[str, Any]], minimum_should_match: int = 1
    ) -> Dict[str, Any]:
        """Build a bool query with should conditions"""
        return {
            "bool": {"should": conditions, "minimum_should_match": minimum_should_match}
        }

    @staticmethod
    def bool_must_not(conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build a bool query with must_not conditions"""
        return {"bool": {"must_not": conditions}}

    @staticmethod
    def sort_by(field: str, order: str = "asc") -> List[Dict[str, Any]]:
        """Build a sort clause"""
        return [{field: {"order": order}}]

    @staticmethod
    def build_query(query_body: Dict[str, Any]) -> Dict[str, Any]:
        """Wrap query body in standard query structure"""
        return {"query": query_body}


class TreeQueryBuilder:
    """Specialized query builder for tree operations"""

    @staticmethod
    def find_children_by_parent(
        parent_obj_id: str, parent_inst_id: int
    ) -> Dict[str, Any]:
        """Build query to find children of a specific parent node"""
        nested_conditions = [
            ESQueryBuilder.term("cw__relation.type", 2),
            ESQueryBuilder.term("cw__relation.bk_asst_obj_id", parent_obj_id),
            ESQueryBuilder.term("cw__relation.bk_asst_inst_id", str(parent_inst_id)),
        ]

        nested_query = ESQueryBuilder.nested(
            "cw__relation", ESQueryBuilder.bool_must(nested_conditions)
        )

        return ESQueryBuilder.build_query(ESQueryBuilder.bool_must([nested_query]))

    @staticmethod
    def add_filters_to_query(
        query: Dict[str, Any], filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add additional term filters to an existing query"""
        if not filters:
            return query

        # Extract existing must conditions
        must_conditions = query["query"]["bool"]["must"]

        # Add term filters for each filter key-value pair
        for key, value in filters.items():
            must_conditions.append(ESQueryBuilder.term(key, value))

        return query

    @staticmethod
    def get_latest_id() -> Dict[str, Any]:
        """Build query to get the document with the highest bk_inst_id"""
        return {"size": 1, "sort": ESQueryBuilder.sort_by("bk_inst_id", "desc")}

    @staticmethod
    def find_by_status(status: int) -> Dict[str, Any]:
        """Build query to find nodes by status"""
        return ESQueryBuilder.build_query(ESQueryBuilder.term("cw_status", status))

    @staticmethod
    def find_by_service_binding(service_inst_id: int) -> Dict[str, Any]:
        """Build query to find nodes bound to a specific service instance"""
        nested_conditions = [
            ESQueryBuilder.term("cw__relation.type", 1),
            ESQueryBuilder.term("cw__relation.bk_asst_inst_id", service_inst_id),
        ]

        nested_query = ESQueryBuilder.nested(
            "cw__relation", ESQueryBuilder.bool_must(nested_conditions)
        )

        return ESQueryBuilder.build_query(ESQueryBuilder.bool_must([nested_query]))


class IndexMappingBuilder:
    """Builder for Elasticsearch index mappings"""

    @staticmethod
    def build_tree_node_mapping() -> Dict[str, Any]:
        """Build the mapping for tree node indices"""
        return {
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
                                    "bk_asst_id": {"type": "keyword"},
                                }
                            },
                            "bk_asst_obj_id": {"type": "keyword"},
                            "bk_asst_inst_id": {"type": "keyword"},
                        },
                    },
                }
            }
        }

    @staticmethod
    def build_object_model_mapping() -> Dict[str, Any]:
        """Build the mapping for object model index"""
        return {
            "mappings": {
                "properties": {
                    "bk_obj_id": {"type": "keyword"},
                    "bk_obj_name": {"type": "keyword"},
                    "properties": {"type": "object"},
                }
            }
        }
