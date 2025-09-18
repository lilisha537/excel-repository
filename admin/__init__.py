from dataclasses  import dataclass,field
from collections import namedtuple

import dataclasses
from  libs import ApiInfo


# api_info_temple = namedtuple(
#     'api_info',["method","url","params",
#      "body","code","resp_body"]
#    ) #元组类型  类型名确定

api_info :dict["str",ApiInfo]=dict(
    验证API=ApiInfo(
        method="GET",
        url="/admin",
    ),
    用户列表=ApiInfo(
        method="GET",
        url="/admin/user",
        params={
            "page":0,
            "size":50,
        },
        resp_body={
            "items":[
                { "复制接口内容"}
            ]
        },
    ),
    添加用户=ApiInfo(
        method="POST",
        url="/admin/user",
        body={"password":"string","email":"user@example.com"},
        code=201,
        resp_body={"items":[
                { "复制接口内容"}
            ]
        },
    ),
    用户详情=ApiInfo(
        method="GET",
        url="/admin/user/{user_id}",
        resp_body={"items":[
                { "复制接口内容"}
            ]
        },
    ),
    修改用户=ApiInfo(
        method="PUT",
        url="/admin/user{user_id}",
        body={"password":"string","email":"user@example.com"},
        resp_body={"items":
                { "复制接口内容"}
        },
    ),
    删除用户=ApiInfo(
        method="DELETE",
        url="/admin/user/{user_id}",
        body={"password":"string","email":"user@example.com"},
        code=204,
    ),
    任务列表=ApiInfo(
        method="GET",
        url="/admin/todo",
        resp_body={"items":
                { "复制接口内容"}
            },
    ),
    添加任务=ApiInfo(
        method="POST",
        url="/admin/todo",
        resp_body={"items":
                { "复制接口内容"}
            },
    ),
    任务详情=ApiInfo(
        method="GET",
        url="/admin/todo/{todo_id}",
        resp_body={"items":
                       {"复制接口内容"}
                   },
    ),
    修改任务=ApiInfo(
        method="PUT",
        url="/admin/todo/{todo_id}",
        resp_body={"items":
                { "复制接口内容"}
            },
    ),
    删除任务=ApiInfo(
        method="DELETE",
        url="/admin/todo/{todo_id}",
        code=200
    ),
)


# api_name='验证API'
# print(api_info["api_name"].method)