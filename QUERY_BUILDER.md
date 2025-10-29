# Elasticsearch Query Builder

This document describes the query builder pattern implemented for improved maintainability of Elasticsearch queries.

## Overview

The query builder provides a clean, maintainable way to construct Elasticsearch queries without hardcoded dictionaries scattered throughout the codebase.

## Components

### 1. ESQueryBuilder (Base Query Builder)

Provides basic building blocks for Elasticsearch queries:

```python
from app.services.query_builder import ESQueryBuilder

# Match all documents
query = ESQueryBuilder.match_all()

# Term query (exact match)
query = ESQueryBuilder.term("cw_status", 10)

# Nested query
nested = ESQueryBuilder.nested("cw__relation", {
    "term": {"cw__relation.type": 2}
})

# Boolean queries
must_query = ESQueryBuilder.bool_must([condition1, condition2])
should_query = ESQueryBuilder.bool_should([condition1, condition2])
```

### 2. TreeQueryBuilder (Domain-Specific Queries)

Provides high-level methods for common tree operations:

```python
from app.services.query_builder import TreeQueryBuilder

# Find children of a parent node
query = TreeQueryBuilder.find_children_by_parent("server", 1)

# Add filters to existing query
filtered = TreeQueryBuilder.add_filters_to_query(query, {"cw_status": 10})

# Get latest ID query
latest = TreeQueryBuilder.get_latest_id()

# Find by status
status_query = TreeQueryBuilder.find_by_status(10)

# Find nodes with service binding
service_query = TreeQueryBuilder.find_by_service_binding(100)
```

### 3. IndexMappingBuilder (Index Mappings)

Provides reusable index mapping definitions:

```python
from app.services.query_builder import IndexMappingBuilder

# Get tree node mapping
mapping = IndexMappingBuilder.build_tree_node_mapping()

# Get object model mapping
mapping = IndexMappingBuilder.build_object_model_mapping()
```

## Benefits

### Before (Hardcoded Queries)

```python
# Hard to read and maintain
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
```

### After (Query Builder)

```python
# Clear, maintainable, reusable
query = TreeQueryBuilder.find_children_by_parent(parent_obj_id, parent_inst_id)
```

## Advantages

1. **Readability**: Method names clearly express intent
2. **Maintainability**: Changes to query structure in one place
3. **Reusability**: Common queries defined once, used everywhere
4. **Testability**: Easy to unit test query construction
5. **Type Safety**: Better IDE support and type hints
6. **Documentation**: Self-documenting code

## Usage Examples

### Finding Children with Filters

```python
# Base query for children
query = TreeQueryBuilder.find_children_by_parent("server", 1)

# Add status filter
query = TreeQueryBuilder.add_filters_to_query(query, {
    "cw_status": 10,
    "region": "us-east-1"
})

# Execute query
result = es_service.search_documents("server", query, page=1, page_size=20)
```

### Creating Index with Mapping

```python
# Get standard mapping
mapping = IndexMappingBuilder.build_tree_node_mapping()

# Create index
es_service.client.indices.create(index="cwcc-server", body=mapping)
```

### Custom Queries

For custom queries not covered by builders, you can still use the base builder:

```python
# Combine multiple conditions
conditions = [
    ESQueryBuilder.term("cw_status", 10),
    ESQueryBuilder.nested("cw__relation", 
        ESQueryBuilder.term("cw__relation.type", 1)
    )
]

query = ESQueryBuilder.build_query(
    ESQueryBuilder.bool_must(conditions)
)
```

## Extending the Builder

To add new query patterns:

1. Add to `ESQueryBuilder` for generic patterns
2. Add to `TreeQueryBuilder` for tree-specific patterns
3. Add to `IndexMappingBuilder` for new index types

Example:

```python
class TreeQueryBuilder:
    @staticmethod
    def find_by_name_prefix(name_prefix: str) -> Dict[str, Any]:
        """Build query to find nodes by name prefix"""
        return ESQueryBuilder.build_query({
            "prefix": {"bk_inst_name": name_prefix}
        })
```

## Testing

All query builders are tested to ensure they produce correct Elasticsearch DSL:

```bash
python3 -c "from app.services.query_builder import *; # test code"
```

## Migration Guide

When updating existing code:

1. Import the query builder: `from app.services.query_builder import TreeQueryBuilder`
2. Replace hardcoded query dictionaries with builder methods
3. Test that queries produce the same results
4. Remove old query code

## References

- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
- [Nested Queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-nested-query.html)
- [Boolean Queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
