# 数据放在 es 中
索引的格式是cwcc-{bk_obj_id}, bk_obj_id 是一个参数
数据的格式是
```json
{
    "bk_inst_id":1,
    "bk_inst_name":"name",
      ......
    "cw_status":1,
    "cw__relation":[
    {
        "type":1|2,// 1: cmdb inst asst, 2: relation（ parent_inst_id,parent_obj_id 出现在子数据上）
        "inst_asst":{
            "bk_obj_asst_id":"",
            "bk_asst_id":"",
        },
        "bk_asst_obj_id":"",
        "bk_asst_inst_id":""
    }
    ]
}
```
关系字段 cw__relation 要明确设置成 nested。 结构参考后面
数据建立统一生存周期字段cw_status（1: add ,10: runing, 11: paused, 12:  run 20: delete）


# 需要实现以下 API
## 层级操作	
### 新建 	POST/api/tree/{type}
### 更新 	PUT/api/tree/{type}
### 删除 	DELETE/api/tree/{type}
### 移动 	POST/api/tree/{type}/move
### 复制 	POST/api/tree/{type}/copy
### 列表 	POST/api/tree/{tree_id}/{parent_obj_id}/{parent_inst_id}/list
## 服务节点数据绑定	
### 绑定 	POST/api/tree/service/inst/bind
### 接班 	POST/api/tree/service/inst/unbind
## 层级节点模型	
### list 	POST/api/model/tree/object/list
### 创建 	POST/api/model/tree/object
