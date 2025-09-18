from collections import namedtuple

import params
import pytest
from libs import ApiInfo

# session =APISession("http://127.0.0.1:8080/")
# 
# ApiInfo = namedtuple(
#     'api_info',["method","url","params",
#      "body","code","resp_body"]
#    ) #元组类型

# user_info = dict(email="ls@qq.com",password="qazxcvbnm0")


#前置条件：列表满足多少条数据
@pytest.fixture()
def user_todo_total(user_session):

    #临时代码：清空之前的数据,验证如果不满足10条 要求则添加数据到min_total
   #  api_name = "清空任务"
   # resp = user_session.request(
   #      api_info[api_name].method,
   #      api_info[api_name].url,
   #      params=api_info[api_name].params,
   # )
   #  assert resp.status_code == 204,resp.json()
   #

    min_total = 10  #要求最少10条数据
    api_name = "任务列表"
    resp = user_session.request(api_info[api_name].method,api_info[api_name].url)

    assert resp.status_code == 200

    total = resp.json()["total"]  #当前数据条数
    if total >= min_total:
        return total
    else:
        #如果不满足10条 要求则添加数据到min_total
        for i in range(min_total - total):
            api_name = "创建任务"
            resp = user_session.request(
                api_info[api_name].method,api_info[api_name].url,json={}
            )
            assert resp.status_code ==200,resp.json()

            return min_total


@pytest.fixture()
def new_todo(user_session):
    api_name="创建任务"
    resp = user_session.request(
        api_info[api_name].method, api_info[api_name].url,json={}
    )

    return resp.json()



api_info :dict["str",ApiInfo]=dict(
    任务列表=ApiInfo(
        method="GET",
        url="/todo",
        params={"page":0,"size":50},  #分页参数，选填

        code=200,
        resp_body={ #接口文档复制内容过来
        },
  ),
    创建任务=ApiInfo(
        method="POST",
        url="/todo",

        body={"title":"null","is_done":False},
        code=200,
        resp_body={ #接口文档复制内容过来
        },
  ),
    清空任务=ApiInfo(
        method="DELETE",
        url="/todo",
        params= {"all":"all"},

        code=204,

  ),
    任务详情=ApiInfo(
        method="GET",
        url="/todo/{todo_id}",

        code=200,
        resp_body={  # 接口文档复制内容过来
        },
    ),
   修改任务=ApiInfo(
        method="PUT",
        url="/todo/{todo_id}",

        body={"title":"null","is_done":False},
        code=204,
        resp_body={ #接口文档复制内容过来
        },
  ),
    删除任务=ApiInfo(
        method="DELETE",
        url="/todo/{todo_id}",

        code=204,

  ),
)




#第一，没有加夹具，使用普通sess的操作 def test_todo_list():  resp=session.request()
#第二，使用夹具，表示已经属于使用已登录session状态，def test_todo_list(user_session):  resp=user_session.request()
def test_todo_list(user_session):
    api_name = "任务列表"

    resp = user_session.request(api_info[api_name].method,api_info[api_name].url,)

    assert resp.status_code == api_info[api_name].code
    assert resp.json().keys() == api_info[api_name].resp_body.keys()


def test_todo_list_401(session):
    api_name="任务列表"
    resp = session.request(api_info[api_name].method, api_info[api_name].url, )

    assert resp.status_code == 401


@pytest.mark.parametrize(
    "params",
    [
        { },
        api_info["任务列表"].params,
        {"size":20,"page":10},
    ],
)

def test_todo_list_params(user_session,params):
    api_name = "任务列表"
    params = api_info[api_name] #1、传入默认get参数，查询字符串  2、 params={ } 传入空参数
    # 3、params=api_info[api_name]  params["size'] = 20  params["page"] =2

    resp = user_session.request(api_info[api_name].method,api_info[api_name].url,params=params)

    assert resp.status_code == api_info[api_name].code
    assert resp.json().keys() == api_info[api_name].resp_body.keys()


@pytest.mark.parametrize(
    "params",
    [
        {"size":1,"page":1},
        {"size":1,"page":2},
        {"size":1,"page":3},
        {"size":2,"page":1},
        {"size":3,"page":1},
        {"size":4,"page":1},
    ],
)

def test_todo_list_size_join_page(user_session,params,user_todo_total):
    """
    测试size和page参数的组合效果
    前置条件：有10条数据
    执行动作：size=1,page=1
    预期结果:todo[:1]
    执行动作：size=1,page=2
    预期结果:todo[:2]
   执行动作：size=2,page=1
    预期结果:todo[:2]
    执行动作：size=2,page=2
    预期结果:todo[:4]
    """

    api_name="任务列表"
    resp = user_session.request(
            api_info[api_name].method, api_info[api_name].url,params=params
        )

    # resp = session.get("http://127.0.0.1:8080/todo",
    #                header={
    #                    "Authorization":"Bearer eyJhbGcioidslvfndlOjnNKDnjkGJJkdcHYid"},
    #                params=params,
    #                )

    assert resp.status_code==200
    resp_body = resp.json()
    assert resp_body["total"] ==user_todo_total
    assert resp_body["page"] == params["page"]
    assert resp_body["size"] ==params["size"]
    assert len(resp_body["items"]) <= params["size"]


@pytest.mark.parametrize(
        "data",
        [
            {},
            {"tile": "我是哈拉哈拉", "is_done": True},
            {"tile": "我是哈拉哈拉1212"},
            {"is_done": True},
        ],
    )

def test_todo_create_success_option(user_session,data):
        api_name = "创建任务"
        resp = user_session.request(
            api_info[api_name].method, api_info[api_name].url, json=data
        )
        assert resp.status_code == api_info[api_name].code
        assert resp.json().keys() == api_info[api_name].resp_body.keys()
        assert resp.json()["title"] == data.get("title", "null")  # 如果没有title，使用默认值null
        assert resp.json()["is_done"] == data.get("is_done", False)  # 如果没有is_done,使用默认值False


def test_todo_delete_all(user_session,user_todo_total):
    api_name = "清空任务"

    resp = user_session.request(
        api_info[api_name].method,
        api_info[api_name].url,
        params=api_info[api_name].params,
    )

    assert resp.status_code == api_info[api_name].code

    api_name = "任务列表"
    resp = user_session.request(
        api_info[api_name].method,
        api_info[api_name].url,
    )

    assert resp.status_code == api_info[api_name].code
    assert resp.json()["total"] ==0   #清空任务之后，任务列表返回的数据量为0



def test_todo_get_success(user_session,new_todo):
    api_name="任务详情"

    resp= user_session.request(
                api_info[api_name].method,api_info[api_name].url.format(todo_id=new_todo['id']),
            )
    assert resp.status_code ==api_info[api_name].code,resp.json() #报错打印日志
    assert resp.json()==new_todo



    #/todo/{todo_id} 任务详情、修改任务等接口测试

@pytest.mark.parametrize(
    "todo_id,code",
    [(0,404),(-1,404),("sanamn",422),("",200)],
)

def test_todo_get_fail(user_session,todo_id,code):
    api_name="任务详情"

    resp = user_session.request(
        api_info[api_name].method, api_info[api_name].url.format(todo_id=-1),
    )
    assert resp.status_code == code, resp.json()  # 报错打印日志


def test_todo_change(user_session,new_todo):
    api_name="修改任务"

    change_todo ={
        "title":new_todo['title']+"_changed",
        "is_done":not new_todo['is_done'],
    }

    resp = user_session.request(
        api_info[api_name].method, api_info[api_name].url.format(todo_id=new_todo['id']),
        json=change_todo,
    )
    assert resp.status_code == api_info[api_name].code, resp.json()  # 报错打印日志
    assert resp.json() ["id"] == new_todo["id"]   #id不变
    assert resp.json()["title"] == new_todo["title"]  #title变化
    assert resp.json()["is_done"] == new_todo["is_done"]   #is_done 变化

    #通过查看任务详情，验证任务title的变化
    api_name = "任务详情"

    resp = user_session.request(
        api_info[api_name].method,
        api_info[api_name].url.format(todo_id=new_todo['id']),
    )
    assert resp.status_code == 200, resp.json()  # 报错打印日志
    assert resp.json() != new_todo




def test_todo_delete(user_session,new_todo):
    api_name = "删除任务"

    resp = user_session.request(
        api_info[api_name].method, api_info[api_name].url.format(todo_id=new_todo['id']),
    )

    assert resp.status_code == api_info[api_name].code, resp.json()  # 报错打印日志

    #断言该任务不存在，查看任务是否存在
    api_name = "任务详情"

    resp = user_session.request(
        api_info[api_name].method,
        api_info[api_name].url.format(todo_id=new_todo['id']),
    )
    assert resp.status_code == 404, resp.json()  # 报错打印日志






