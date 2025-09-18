import pytest
from  libs import APISession,ApiInfo

class ApiList:
    获取验证码 = ApiInfo(
        method="POST",
        url="/account/sendValidCodeTest",
        body={"forceSend":True,"operateType":2,"phone":" "},
                         )

    登录=ApiInfo(
        method="POST",
        url="/account/login",
        params={"loginType":1,
                "terminalType":0,
                "phone":" ",
                "msgCode":" ",

                },
    )

    用户基本信息=ApiInfo(
        method="GET",
        url="/user/simpleInfo",
    )
    用户详细信息=ApiInfo(
        method="GET",
        url="/user/detailInfo"
    )
    最后一次学习=ApiInfo(
        method="GET",
        url="/v2/study/lastRecord"
    )
    我的课程列表=ApiInfo(
        method="POST",
        url="/v2/study/myList",params={"filter":0,"pageIndex":1,"pageSize":10 }
    )

    更新用户基本信息 = ApiInfo(
        method="POST",
        url="/user/updateUserInfo",
    )

    上传文件 = ApiInfo(
        method="POST",
        url="/crm/upload/addFile",

    )



_api_info =ApiList()  #变量
_base_url="http://47.93.233.188:200"
_user_info={"phone":"13800000001"}  #测试账号





@pytest.fixture(scope="session")
def api_info():
    return _api_info


@pytest.fixture(scope="session")
def session():
    """未登录状态的session"""

    return APISession(base_url=_base_url)



@pytest.fixture(scope="session")
def user_session(api_info):
    """已登录的session"""
    session = APISession(base_url=_base_url)
    #1.登录获取token
    #1.1 获取验证码
    api = api_info.获取验证码
    data =api.body  #设置传递的参数
    data["phone"] = _user_info["phone"]
    resp = session.request(api.method,api.url,json=data)
    assert resp.status_code==api.code
    assert resp.json().keys() == api.resp_body.keys()
    assert resp.json()["code"] == 0

    msgCode = resp.json()["data"]  #短信验证码


    # 1.2 获取token
    api = api_info.登录
    data = api.params  # 设置传递的参数
    data["phone"] = _user_info["phone"]  #手机号
    data["msgCode"] =msgCode #短信验证码
    resp = session.request(api.method, api.url, params=data)
    assert resp.status_code == api.code
    assert resp.json().keys() == api.resp_body.keys()
    assert resp.json()["code"] == 0

    token = resp.json()["data"]  # token


    #2.把token添加到session请求头
    session.headers["token"] = token

    return session



