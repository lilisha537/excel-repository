#这里创建的夹具供admin包内的用例使用
#如果创建了一个和上级目录conftest中的同名夹具,,以当前为准
import time

import pytest

from . import api_info


@pytest.fixture()
def admin_session(session):
    session.headers["X-API-KEY"] = "5dfnk6DUHK+"
    yield session


session.headers.pop("X-API-KEY")


@pytest.fixture()
def new_user():
    #创建一个用户
    api_name="添加用户"
    email=f"{time.time():.2f}@q.c"  #生成基于时间戳的账号，确保不会重复
    data = {"password": email, "email":email}  #todo
    resp = admin_session.request(api_info[api_name].method, api_info[api_name].url, json=data
                             )
    assert resp.status_code == api_info[api_name].code
    yield resp.json() #返回刚创建的用户

#测试结束后销毁数据
    api_name="删除用户"

    resp = admin_session.request(api_info[api_name].method, api_info[api_name].url, json=data
                             )
    assert resp.status_code == api_info[api_name].code





@pytest.fixture()
def new_todo(admin_session,new_user):
    """
    创建一个新的任务，
    :return:
    """
    api_name="添加任务"
    data={"title":"null","is_done":False,"user_id":new_user["id"]}
    resp = admin_session.request(api_info[api_name].method,api_info[api_name].url,json=data
                                 )
    assert resp.status_code == api_info[api_name].code
    yield resp.json()  #返回创建的任务


#测试结束后销毁数据，需要兼容数据在用例中被删除的情况
    api_name = "删除任务"

    resp = admin_session.request(api_info[api_name].method, api_info[api_name].url.format(todo_id=resp.json['id']),
                                 )
    assert resp.status_code in (api_info[api_name].code,404),resp.json()
    yield resp.json()  # 返回创建的任务
    

#前置条件：列表满足多少条数据
@pytest.fixture()
def todo_total(admin_session,new_user):

    min_total = 10  #要求最少10条数据
    api_name = "任务列表"
    resp = admin_session.request(api_info[api_name].method,api_info[api_name].url)

    assert resp.status_code == 200

    total = resp.json()["total"]  #当前数据条数
    if total >= min_total:
        return total
    else:
        #如果不满足10条 要求则添加数据到min_total
        for i in range(min_total - total):
            api_name = "添加任务"
            data = {"title": "null", "is_done": False, "user_id": new_user["id"]}
            resp = admin_session.request(
                api_info[api_name].method,api_info[api_name].url,json=data
            )
            assert resp.status_code ==201,resp.json()

            return min_total