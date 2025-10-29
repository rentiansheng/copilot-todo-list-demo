# API Usage Examples

This document provides example curl commands for all API endpoints.

## Prerequisites

1. Start the API server: `./start.sh` or `uvicorn main:app --reload`
2. Ensure Elasticsearch is running and accessible

## Tree Operations

### 1. Create a Tree Object Model First

```bash
curl -X POST "http://localhost:8000/api/model/tree/object" \
  -H "Content-Type: application/json" \
  -d '{
    "bk_obj_id": "server",
    "bk_obj_name": "Server",
    "properties": {
      "cpu": "string",
      "memory": "string"
    }
  }'
```

### 2. Create Root Tree Node

```bash
curl -X POST "http://localhost:8000/api/tree/server" \
  -H "Content-Type: application/json" \
  -d '{
    "bk_inst_name": "Root Server",
    "bk_obj_id": "server",
    "additional_fields": {
      "cpu": "Intel i7",
      "memory": "16GB"
    }
  }'
```

### 3. Create Child Tree Node

```bash
curl -X POST "http://localhost:8000/api/tree/server" \
  -H "Content-Type: application/json" \
  -d '{
    "bk_inst_name": "Child Server",
    "bk_obj_id": "server",
    "parent_obj_id": "server",
    "parent_inst_id": 1,
    "additional_fields": {
      "cpu": "Intel i5",
      "memory": "8GB"
    }
  }'
```

### 4. Update Tree Node

```bash
curl -X PUT "http://localhost:8000/api/tree/server" \
  -H "Content-Type: application/json" \
  -d '{
    "bk_inst_id": 1,
    "bk_obj_id": "server",
    "bk_inst_name": "Updated Root Server",
    "cw_status": 10,
    "additional_fields": {
      "cpu": "Intel i9"
    }
  }'
```

### 5. List Child Nodes

```bash
curl -X POST "http://localhost:8000/api/tree/server/server/1/list" \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "page_size": 20,
    "filters": {}
  }'
```

### 6. Move Tree Node

```bash
curl -X POST "http://localhost:8000/api/tree/server/move" \
  -H "Content-Type: application/json" \
  -d '{
    "bk_inst_id": 2,
    "bk_obj_id": "server",
    "target_parent_obj_id": "server",
    "target_parent_inst_id": 3
  }'
```

### 7. Copy Tree Node

```bash
curl -X POST "http://localhost:8000/api/tree/server/copy" \
  -H "Content-Type: application/json" \
  -d '{
    "bk_inst_id": 1,
    "bk_obj_id": "server",
    "target_parent_obj_id": "server",
    "target_parent_inst_id": 2,
    "new_inst_name": "Copied Server"
  }'
```

### 8. Delete Tree Node (Soft Delete)

```bash
curl -X DELETE "http://localhost:8000/api/tree/server" \
  -H "Content-Type: application/json" \
  -d '{
    "bk_obj_id": "server",
    "bk_inst_id": 2
  }'
```

## Service Instance Binding

### 9. Bind Service Instance

```bash
curl -X POST "http://localhost:8000/api/tree/service/inst/bind" \
  -H "Content-Type: application/json" \
  -d '{
    "service_inst_id": 100,
    "bk_inst_id": 1,
    "bk_obj_id": "server"
  }'
```

### 10. Unbind Service Instance

```bash
curl -X POST "http://localhost:8000/api/tree/service/inst/unbind" \
  -H "Content-Type: application/json" \
  -d '{
    "service_inst_id": 100,
    "bk_inst_id": 1,
    "bk_obj_id": "server"
  }'
```

## Tree Object Model Operations

### 11. List All Object Models

```bash
curl -X POST "http://localhost:8000/api/model/tree/object/list" \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "page_size": 20
  }'
```

## Testing with Python

You can also use Python to test the API:

```python
import requests

BASE_URL = "http://localhost:8000"

# Create object model
response = requests.post(
    f"{BASE_URL}/api/model/tree/object",
    json={
        "bk_obj_id": "server",
        "bk_obj_name": "Server",
        "properties": {"cpu": "string", "memory": "string"}
    }
)
print(response.json())

# Create tree node
response = requests.post(
    f"{BASE_URL}/api/tree/server",
    json={
        "bk_inst_name": "My Server",
        "bk_obj_id": "server",
        "additional_fields": {"cpu": "Intel i7", "memory": "16GB"}
    }
)
print(response.json())
```

## Response Format

All API endpoints return responses in the following format:

```json
{
  "code": 0,
  "data": { ... },
  "message": "success"
}
```

- `code`: 0 for success, non-zero for errors
- `data`: Response data (varies by endpoint)
- `message`: Human-readable message

## Status Codes

HTTP status codes:
- `200`: Success
- `400`: Bad Request (with error details in response)
- `500`: Internal Server Error
