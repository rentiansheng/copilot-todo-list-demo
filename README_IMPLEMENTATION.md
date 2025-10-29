# CMDB Tree API Implementation

本项目实现了基于 Elasticsearch 的 CMDB 树形结构管理 API。

## 数据存储

数据存储在 Elasticsearch 中：
- 索引格式：`cwcc-{bk_obj_id}`，其中 `bk_obj_id` 是对象类型参数
- 关系字段 `cw__relation` 设置为 nested 类型
- 数据生命周期字段 `cw_status`：
  - 1: add (添加)
  - 10: running (运行中)
  - 11: paused (暂停)
  - 12: run (运行)
  - 20: delete (删除)

## 数据格式

```json
{
    "bk_inst_id": 1,
    "bk_inst_name": "name",
    "cw_status": 1,
    "cw__relation": [
        {
            "type": 1,  // 1: cmdb inst asst, 2: relation
            "inst_asst": {
                "bk_obj_asst_id": "",
                "bk_asst_id": ""
            },
            "bk_asst_obj_id": "",
            "bk_asst_inst_id": 0
        }
    ]
}
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并配置 Elasticsearch 连接：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```
ELASTICSEARCH_HOST=localhost:9200
ELASTICSEARCH_USER=elastic
ELASTICSEARCH_PASSWORD=your_password
```

### 3. 启动服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后访问：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## API 接口

### 层级操作

#### 1. 新建树节点
```http
POST /api/tree/{type}
Content-Type: application/json

{
    "bk_inst_name": "节点名称",
    "parent_obj_id": "parent_type",
    "parent_inst_id": 1,
    "properties": {
        "custom_field": "value"
    }
}
```

#### 2. 更新树节点
```http
PUT /api/tree/{type}
Content-Type: application/json

{
    "bk_inst_id": 1,
    "bk_inst_name": "新名称",
    "cw_status": 10
}
```

#### 3. 删除树节点
```http
DELETE /api/tree/{type}
Content-Type: application/json

{
    "bk_inst_id": 1
}
```

#### 4. 移动树节点
```http
POST /api/tree/{type}/move
Content-Type: application/json

{
    "bk_inst_id": 1,
    "target_parent_obj_id": "new_parent_type",
    "target_parent_inst_id": 2
}
```

#### 5. 复制树节点
```http
POST /api/tree/{type}/copy
Content-Type: application/json

{
    "bk_inst_id": 1,
    "target_parent_obj_id": "parent_type",
    "target_parent_inst_id": 2,
    "new_inst_name": "复制的节点"
}
```

#### 6. 列表查询
```http
POST /api/tree/{tree_id}/{parent_obj_id}/{parent_inst_id}/list
Content-Type: application/json

{
    "page": 1,
    "page_size": 20,
    "filter": {
        "field": "value"
    }
}
```

### 服务节点数据绑定

#### 1. 绑定
```http
POST /api/tree/service/inst/bind
Content-Type: application/json

{
    "service_obj_id": "service",
    "service_inst_id": 1,
    "target_obj_id": "target",
    "target_inst_id": 2
}
```

#### 2. 解绑
```http
POST /api/tree/service/inst/unbind
Content-Type: application/json

{
    "service_obj_id": "service",
    "service_inst_id": 1,
    "target_obj_id": "target",
    "target_inst_id": 2
}
```

### 层级节点模型

#### 1. 创建对象模型
```http
POST /api/model/tree/object
Content-Type: application/json

{
    "bk_obj_id": "host",
    "bk_obj_name": "主机",
    "properties": {
        "description": "主机对象"
    }
}
```

#### 2. 查询对象模型列表
```http
POST /api/model/tree/object/list
Content-Type: application/json

{
    "page": 1,
    "page_size": 20,
    "filter": {
        "bk_obj_id": "host"
    }
}
```

## 项目结构

```
.
├── main.py                 # 应用入口
├── requirements.txt        # Python 依赖
├── .env.example           # 环境变量示例
├── .gitignore            # Git 忽略文件
└── app/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   └── routes/
    │       ├── __init__.py
    │       ├── tree.py    # 树操作路由
    │       └── model.py   # 模型操作路由
    ├── core/
    │   ├── __init__.py
    │   ├── config.py      # 配置管理
    │   └── elasticsearch.py  # ES 客户端
    ├── models/
    │   ├── __init__.py
    │   └── schemas.py     # 数据模型
    └── services/
        ├── __init__.py
        ├── tree_service.py        # 树操作服务
        ├── service_bind_service.py # 绑定操作服务
        └── model_service.py       # 模型操作服务
```

## 技术栈

- **FastAPI**: 现代、高性能的 Python Web 框架
- **Elasticsearch**: 分布式搜索和分析引擎
- **Pydantic**: 数据验证和设置管理
- **Uvicorn**: ASGI 服务器

## 注意事项

1. 确保 Elasticsearch 服务已启动并可访问
2. 首次运行时会自动创建必要的索引和映射
3. 所有删除操作都是软删除，通过设置 `cw_status=20` 实现
4. 关系字段 `cw__relation` 使用 nested 类型存储，支持复杂查询
