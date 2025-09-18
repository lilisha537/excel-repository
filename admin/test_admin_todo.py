from . import api_info
import pytest


from libs import APISession

session =APISession("http://127.0.0.1:8080/")


def test_todo_list(admin_session):
    api_name = "任务列表"

    resp = admin_session.request(api_info[api_name].method,api_info[api_name].url,)

    assert resp.status_code == api_info[api_name].code
    assert resp.json().keys() == api_info[api_name].resp_body.keys()


@pytest.mark.parametrize(
    "params",
    [
        { },
        api_info["任务列表"].params,
        {"size":20,"page":10},
    ],
)

def test_todo_list_params(admin_session,params):
    api_name = "任务列表"
    params = api_info[api_name] #1、传入默认get参数，查询字符串  2、 params={ } 传入空参数
    # 3、params=api_info[api_name]  params["size'] = 20  params["page"] =2

    resp = admin_session.request(api_info[api_name].method,api_info[api_name].url,params=params)

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

def test_todo_list_size_join_page(admin_session,params,todo_total):
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
    api_name="任务列表"    #改良写法
    resp = admin_session.request(api_info[api_name].method,api_info[api_name].url,params=params)

    # 原始写法
    # resp = session.get(
    #     "http://127.0.0.1:8080/todo",
    #                params=params,
    #                )

    assert resp.status_code==200,resp.json()
    resp_body = resp.json()
    assert resp_body["total"] ==todo_total
    assert resp_body["page"] == params["page"]
    assert resp_body["size"] ==params["size"]
    assert len(resp_body["items"]) <= params["size"]


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"tile":"我是哈拉哈拉","is_done":True},
        {"tile":"我是哈拉哈拉1212"},
        {"is_done":True},
    ],
)

def test_todo_create_success_option(admin_session,data,new_user):
    api_name ="添加任务"

    data["user_id"] = new_user["id"]
    resp=admin_session.request(
       api_info[api_name].method,api_info[api_name].url,json=data
    )

    assert resp.status_code ==api_info[api_name].code
    assert resp.json().keys() == api_info[api_name].resp_body.keys()
    assert resp.json()["title"]==data.get("title","null") #如果没有title，使用默认值null
    assert resp.json()["is_done"] == data.get("is_done",False) #如果没有is_done,使用默认值False




    def test_todo_get_success(admin_session,new_todo):
        api_name="任务详情"

        resp= admin_session.request(
                api_info[api_name].method,api_info[api_name].url.format(todo_id=new_todo['id']),
            )
        assert resp.status_code ==api_info[api_name].code,resp.json() #报错打印日志
        assert resp.json()==new_todo



    #/todo/{todo_id} 任务详情、修改任务等接口测试

@pytest.mark.parametrize(
    "todo_id,code",
    [(0,404),(-1,404),("sanamn",422),("",200)],
)

def test_todo_get_fail(admin_session,todo_id,code):
    api_name="任务详情"

    resp = admin_session.request(
        api_info[api_name].method, api_info[api_name].url.format(todo_id=-1),
    )
    assert resp.status_code == code, resp.json()  # 报错打印日志


def test_todo_change(admin_session,new_todo):
    api_name="修改任务"

    change_todo ={
        "title":new_todo['title']+"_changed",
        "is_done":not new_todo['is_done'],
        "user_id":new_todo["user_id"],
    }

    resp = admin_session.request(
        api_info[api_name].method, api_info[api_name].url.format(todo_id=new_todo['id']),
        json=change_todo,
    )
    assert resp.status_code == api_info[api_name].code, resp.json()  # 报错打印日志
    assert resp.json() ["id"] == new_todo["id"]   #id不变
    assert resp.json()["title"] == new_todo["title"]  #title变化
    assert resp.json()["is_done"] == new_todo["is_done"]   #is_done 变化

    #通过查看任务详情，验证任务title的变化
    api_name = "任务详情"

    resp = admin_session.request(
        api_info[api_name].method,
        api_info[api_name].url.format(todo_id=new_todo['id']),
    )
    assert resp.status_code == 200, resp.json()  # 报错打印日志
    assert resp.json() != new_todo




def test_todo_delete(admin_session,new_todo):
    api_name = "删除任务"

    resp = admin_session.request(
        api_info[api_name].method, api_info[api_name].url.format(todo_id=new_todo['id']),
    )

    assert resp.status_code == api_info[api_name].code, resp.json()  # 报错打印日志

    #断言该任务不存在，查看任务是否存在
    api_name = "任务详情"

    resp = admin_session.request(
        api_info[api_name].method,
        api_info[api_name].url.format(todo_id=new_todo['id']),
    )
    assert resp.status_code == 404, resp.json()  # 报错打印日志