import requests


def test_get_user_info(user_session):
    """测试登录用户可以获取用户信息
    通过夹具方式，提供未登录状态的session """

    resp = user_session.request("GET","/user/detailInfo")
    assert resp.status_code == 200
    assert resp.json()["code"] == 0


def test_get_user_info_fail(session):
    """测试未登录用户
    """
    resp = session.request("GET", "/user/detailInfo")
    assert resp.status_code == 200
    assert resp.json()["code"] == 1001

def test_get_user_info_all(user_session,api_info):
    """测试加载用户信息的所有接口响应正常"""

    for api in [
        api_info.用户基本信息,
        api_info.用户详细信息,
        api_info.最后一次学习,
        api_info.我的课程列表,
    ]:
        resp = user_session.request(api.method,api.url,params=api.params,json=api.body)
        assert resp.status_code ==200
        assert resp.json()["code"] == 0
        assert resp.json()["data"]


def test_update_user_info_city(user_session,api_info):
    """
    修改用户基本信息：城市
    :param user_session:
    :param api_info:
    :return:
    """

    city = "北京"

    api = api_info.更新用户基本信息
    data = api.params
    data["city"] = city
    resp = user_session.request(api.method,api.url,params=data)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0,resp.json()


    api = api.info.用户详细信息
    resp = user_session.request(api.method,api.url,params=data)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0,resp.json()
    assert resp.json()["data"]["student"]["city"] == city



def test_update_user_info_headimg(user_session,api_info):
    """
        修改用户头像信息
        1、上传图片获取到图片url
        2、将图片url作为参数进行传递，修改用户信息

        """
    api = api_info.上传文件
    f = open(r"C:\Users\xxxx.png","rb")
    resp = user_session.request(api.method, api.url, files={"file":f})
    assert resp.status_code == 200
    assert resp.json()["code"] == 0, resp.json()


    avater = resp.json()["data"] #头像图片url

    #请求结果
    api = api_info.更新用户基本信息
    data = api.params
    data["avater"] = avater
    resp = user_session.request(api.method, api.url, params=data)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0, resp.json()

    #验证结果
    api = api_info.用户详细信息
    resp = user_session.request(api.method, api.url)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0, resp.json()
    assert resp.json()["data"]["headImg"] == avater




