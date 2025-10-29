from app.services.query_builder import (
    ESQueryBuilder,
    IndexMappingBuilder,
    TreeQueryBuilder,
)


class TestESQueryBuilder:
    """Test cases for ESQueryBuilder"""

    def test_match_all(self):
        """Test match_all query builder"""
        query = ESQueryBuilder.match_all()
        assert query == {"query": {"match_all": {}}}

    def test_term(self):
        """Test term query builder"""
        query = ESQueryBuilder.term("field", "value")
        assert query == {"term": {"field": "value"}}

    def test_terms(self):
        """Test terms query builder"""
        query = ESQueryBuilder.terms("field", ["val1", "val2"])
        assert query == {"terms": {"field": ["val1", "val2"]}}

    def test_nested(self):
        """Test nested query builder"""
        inner_query = {"term": {"nested_field": "value"}}
        query = ESQueryBuilder.nested("my_path", inner_query)
        assert query == {"nested": {"path": "my_path", "query": inner_query}}

    def test_bool_must(self):
        """Test bool must query builder"""
        conditions = [{"term": {"field1": "val1"}}, {"term": {"field2": "val2"}}]
        query = ESQueryBuilder.bool_must(conditions)
        assert query == {"bool": {"must": conditions}}

    def test_bool_should(self):
        """Test bool should query builder"""
        conditions = [{"term": {"field1": "val1"}}]
        query = ESQueryBuilder.bool_should(conditions, minimum_should_match=1)
        assert query == {"bool": {"should": conditions, "minimum_should_match": 1}}

    def test_bool_must_not(self):
        """Test bool must_not query builder"""
        conditions = [{"term": {"field1": "val1"}}]
        query = ESQueryBuilder.bool_must_not(conditions)
        assert query == {"bool": {"must_not": conditions}}

    def test_sort_by_asc(self):
        """Test sort by ascending"""
        sort = ESQueryBuilder.sort_by("field", "asc")
        assert sort == [{"field": {"order": "asc"}}]

    def test_sort_by_desc(self):
        """Test sort by descending"""
        sort = ESQueryBuilder.sort_by("field", "desc")
        assert sort == [{"field": {"order": "desc"}}]

    def test_build_query(self):
        """Test build_query wrapper"""
        query_body = {"term": {"field": "value"}}
        query = ESQueryBuilder.build_query(query_body)
        assert query == {"query": query_body}


class TestTreeQueryBuilder:
    """Test cases for TreeQueryBuilder"""

    def test_find_children_by_parent(self):
        """Test finding children by parent query"""
        query = TreeQueryBuilder.find_children_by_parent("server", 1)

        assert "query" in query
        assert "bool" in query["query"]
        assert "must" in query["query"]["bool"]
        assert len(query["query"]["bool"]["must"]) == 1

        nested = query["query"]["bool"]["must"][0]
        assert nested["nested"]["path"] == "cw__relation"

        nested_conditions = nested["nested"]["query"]["bool"]["must"]
        assert len(nested_conditions) == 3
        assert {"term": {"cw__relation.type": 2}} in nested_conditions
        assert {"term": {"cw__relation.bk_asst_obj_id": "server"}} in nested_conditions
        assert {"term": {"cw__relation.bk_asst_inst_id": "1"}} in nested_conditions

    def test_add_filters_to_query(self):
        """Test adding filters to existing query"""
        base_query = TreeQueryBuilder.find_children_by_parent("server", 1)
        filters = {"cw_status": 10, "region": "us-east"}

        filtered_query = TreeQueryBuilder.add_filters_to_query(base_query, filters)

        must_conditions = filtered_query["query"]["bool"]["must"]
        assert len(must_conditions) == 3  # 1 nested + 2 filters
        assert {"term": {"cw_status": 10}} in must_conditions
        assert {"term": {"region": "us-east"}} in must_conditions

    def test_add_filters_to_query_empty(self):
        """Test adding no filters returns same query"""
        base_query = TreeQueryBuilder.find_children_by_parent("server", 1)
        filtered_query = TreeQueryBuilder.add_filters_to_query(base_query, None)
        assert filtered_query == base_query

    def test_get_latest_id(self):
        """Test get latest ID query"""
        query = TreeQueryBuilder.get_latest_id()
        assert query == {"size": 1, "sort": [{"bk_inst_id": {"order": "desc"}}]}

    def test_find_by_status(self):
        """Test find by status query"""
        query = TreeQueryBuilder.find_by_status(10)
        assert query == {"query": {"term": {"cw_status": 10}}}

    def test_find_by_service_binding(self):
        """Test find by service binding query"""
        query = TreeQueryBuilder.find_by_service_binding(100)

        assert "query" in query
        nested = query["query"]["bool"]["must"][0]
        assert nested["nested"]["path"] == "cw__relation"

        nested_conditions = nested["nested"]["query"]["bool"]["must"]
        assert {"term": {"cw__relation.type": 1}} in nested_conditions
        assert {"term": {"cw__relation.bk_asst_inst_id": 100}} in nested_conditions


class TestIndexMappingBuilder:
    """Test cases for IndexMappingBuilder"""

    def test_build_tree_node_mapping(self):
        """Test building tree node mapping"""
        mapping = IndexMappingBuilder.build_tree_node_mapping()

        assert "mappings" in mapping
        assert "properties" in mapping["mappings"]

        props = mapping["mappings"]["properties"]
        assert "bk_inst_id" in props
        assert props["bk_inst_id"]["type"] == "integer"
        assert "bk_inst_name" in props
        assert props["bk_inst_name"]["type"] == "keyword"
        assert "cw_status" in props
        assert props["cw_status"]["type"] == "integer"

        # Check nested relation field
        assert "cw__relation" in props
        assert props["cw__relation"]["type"] == "nested"
        assert "properties" in props["cw__relation"]

        relation_props = props["cw__relation"]["properties"]
        assert "type" in relation_props
        assert "bk_asst_obj_id" in relation_props
        assert "bk_asst_inst_id" in relation_props
        assert "inst_asst" in relation_props

    def test_build_object_model_mapping(self):
        """Test building object model mapping"""
        mapping = IndexMappingBuilder.build_object_model_mapping()

        assert "mappings" in mapping
        props = mapping["mappings"]["properties"]

        assert "bk_obj_id" in props
        assert props["bk_obj_id"]["type"] == "keyword"
        assert "bk_obj_name" in props
        assert props["bk_obj_name"]["type"] == "keyword"
        assert "properties" in props
        assert props["properties"]["type"] == "object"
