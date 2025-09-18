#pytest配置文件，测试前提前启动
import pytest
from libs import APISession

@pytest.fixture(scope="session")  #每次测试启动，只登陆一次
def session ():
    return APISession("http://127.0.0.1:8080/")


user_info = dict(email="ls@qq.com", password="qazxcv")


@pytest.fixture(scope="session")  #每次测试启动，只登陆一次
def user_token(session):
    resp = session.request(
        method="POST",url="？login/access_token",json=user_info
    )

    assert resp.status_code == 200
    newtoken = resp.json()["access_token"]   #获取新token

    return newtoken

@pytest.fixture()
def user_session(session,user_token):
    session.headers["Authorization"]= "Bearer" +user_token
    yield session
    session.headers.pop("Authorization")

@pytest.fixture()
def admin_session(session):
    session.headers["X-API-KEY"]= "5dfnk6DUHK+"
    print(2)
    yield session
    session.headers.pop("X-API-KEY")


# @pytest.fixture()
# def user_todo_total(user_session):
#
#     #临时代码：清空之前的数据,验证如果不满足10条 要求则添加数据到min_total
#    #  api_name = "清空任务"
#    # resp = user_session.request(
#    #      api_info[api_name].method,
#    #      api_info[api_name].url,
#    #      params=api_info[api_name].params,
#    # )
#    #  assert resp.status_code == 204,resp.json()
#    #
#
#     min_total = 10  #要求最少10条数据
#     api_name = "任务列表"
#     resp = user_session.request("GET","/todo")
#
#     assert resp.status_code == 200
#
#     total = resp.json()["total"]  #当前数据条数
#     if total >= min_total:
#         return total
#     else:
#         #如果不满足10条 要求则添加数据到min_total
#         for i in range(min_total - total):
#             api_name = "创建任务"
#             resp = user_session.request(
#                "POST","/todo",json={}
#             )
#             assert resp.status_code ==200,resp.json()
#
#             return min_total
