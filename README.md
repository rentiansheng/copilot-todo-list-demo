# Tree Management API

A REST API service for managing hierarchical tree structures with Elasticsearch backend.

## Features

- **Tree Operations**: Create, Update, Delete, Move, Copy tree nodes
- **Tree Listing**: List child nodes under a specific parent
- **Service Binding**: Bind/Unbind service instances to tree nodes
- **Object Model Management**: Create and list tree object models
- **Elasticsearch Backend**: Data stored with proper nested relation support

## Requirements

- Python 3.8+
- Elasticsearch 8.x
- Dependencies listed in `requirements.txt`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Elasticsearch connection:
```bash
cp .env.example .env
# Edit .env with your Elasticsearch credentials
```

3. Start Elasticsearch (if running locally):
```bash
# Using Docker
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.11.0
```

## Running the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Tree Operations

#### Create Tree Node
```
POST /api/tree/{type}
```
Body:
```json
{
  "bk_inst_name": "Node Name",
  "bk_obj_id": "object_type",
  "parent_obj_id": "parent_type",
  "parent_inst_id": 1,
  "additional_fields": {}
}
```

#### Update Tree Node
```
PUT /api/tree/{type}
```
Body:
```json
{
  "bk_inst_id": 1,
  "bk_obj_id": "object_type",
  "bk_inst_name": "Updated Name",
  "cw_status": 10
}
```

#### Delete Tree Node
```
DELETE /api/tree/{type}
```
Body:
```json
{
  "bk_obj_id": "object_type",
  "bk_inst_id": 1
}
```

#### Move Tree Node
```
POST /api/tree/{type}/move
```
Body:
```json
{
  "bk_inst_id": 1,
  "bk_obj_id": "object_type",
  "target_parent_obj_id": "new_parent_type",
  "target_parent_inst_id": 2
}
```

#### Copy Tree Node
```
POST /api/tree/{type}/copy
```
Body:
```json
{
  "bk_inst_id": 1,
  "bk_obj_id": "object_type",
  "target_parent_obj_id": "parent_type",
  "target_parent_inst_id": 2,
  "new_inst_name": "Copied Node"
}
```

#### List Tree Nodes
```
POST /api/tree/{tree_id}/{parent_obj_id}/{parent_inst_id}/list
```
Body:
```json
{
  "page": 1,
  "page_size": 20,
  "filters": {}
}
```

### Service Instance Binding

#### Bind Service Instance
```
POST /api/tree/service/inst/bind
```
Body:
```json
{
  "service_inst_id": 100,
  "bk_inst_id": 1,
  "bk_obj_id": "object_type"
}
```

#### Unbind Service Instance
```
POST /api/tree/service/inst/unbind
```
Body:
```json
{
  "service_inst_id": 100,
  "bk_inst_id": 1,
  "bk_obj_id": "object_type"
}
```

### Tree Object Model

#### Create Tree Object Model
```
POST /api/model/tree/object
```
Body:
```json
{
  "bk_obj_id": "object_type",
  "bk_obj_name": "Object Name",
  "properties": {}
}
```

#### List Tree Object Models
```
POST /api/model/tree/object/list
```
Body:
```json
{
  "page": 1,
  "page_size": 20
}
```

## Data Structure

### Elasticsearch Index Format
- Index name: `cwcc-{bk_obj_id}`
- Object models index: `cwcc-object-models`

### Document Structure
```json
{
  "bk_inst_id": 1,
  "bk_inst_name": "name",
  "cw_status": 1,
  "cw__relation": [
    {
      "type": 1,
      "inst_asst": {
        "bk_obj_asst_id": "",
        "bk_asst_id": ""
      },
      "bk_asst_obj_id": "",
      "bk_asst_inst_id": ""
    }
  ]
}
```

### Status Values (cw_status)
- `1`: add
- `10`: running
- `11`: paused
- `12`: run
- `20`: delete

### Relation Types
- `1`: CMDB instance association
- `2`: Parent-child relation

## Development

### Project Structure
```
.
├── main.py                 # Application entry point
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration
│   ├── api/               # API routes
│   │   ├── tree.py        # Tree operations
│   │   └── model.py       # Model operations
│   ├── models/            # Data models
│   │   └── schemas.py     # Pydantic schemas
│   └── services/          # Business logic
│       ├── elasticsearch.py    # ES client
│       ├── tree_service.py     # Tree operations
│       └── model_service.py    # Model operations
├── requirements.txt       # Dependencies
└── readme.md             # Documentation
```

## License

MIT
