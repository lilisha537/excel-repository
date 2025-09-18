import requests
from libs import APISession

import allure
import time
from libs import ApiInfo

from conftest import user_info
# session = APISession("http://127.0.0.1:8080/")


api_info :dict["str",ApiInfo]=dict(
    登录=ApiInfo(
         method ="POST",
         url="/login/access_token",
         body={"password":"string","email":"user@example.com"},
         code=200,
         resp_body={"access_token":"string","token+type":"string"},
     ),
    注册=ApiInfo(
        method ="POST",
        url="/login/sign_up",
        body={"password":"string","email":"user@example.com"},
        code=200,
        resp_body={
            "id" :0,
            "email":"user@example.com"
        },
    ),
    token =ApiInfo(
        method="POST",
        url="/login/test_token",
        body={},
        code=200,
        resp_body={},

)
)

@allure.severity(allure.severity_level.CRITICAL)
@allure.title("用例：登录成功")
@allure.description(
"""
前置条件：xxxx<br/>
预期结果：yyyy
"""
)
def test_post_login_success(session):

    api_name="登录"
    resp = session.request(
        method=api_info[api_name].method,url=api_info[api_name].url,json=user_info
    )

    assert resp.status_code == api_info[api_name].code,resp.json()
    assert resp.json().keys() == api_info[api_name].resp_body.keys()


def test_post_login_fail(session):
    """ 使用错误的用户名和密码，登录失败 """
    error_user_info = dict(**user_info)   #复制user_info
    error_user_info["password"] = "error_paswwls@qq.com"

    api_name = "登录"

    resp = session.request(
        method = api_info[api_name].method,url=api_info[api_name].url,json=error_user_info
    )

    assert resp.status_code != api_info[api_name].code,resp.json()


def test_token_success(session):
    """使用登录状态客户端，访问test_token
前置条件：session的请求头有token
测试时自动登录，获取token
测试时手动登录，获取token---不可取
执行动作：发送账号密码到接口
预期结果：响应状态为200
    """
    api_name = "登录"

    resp = session.request(
        method=api_info[api_name].method,url=api_info[api_name].url,json=user_info
    )

    assert resp.status_code == api_info[api_name].code
    newtoken = resp.json()["access_token"]   #获取新token

    session.headers["Authorization"] = "Bearer"+newtoken

    resp = session.request(
     method = api_info.[api_name].method,url=api_info.[api_name].url
    )

    assert  resp.status_code == api_info.[api_name].code



def test_token_fail(session):
    """
    使用未登录状态客户端，访问test_token
    前置条件：session的请求头没有有token
    预期结果响应码 ！= 200
    """

    api_name="TestToken"

    #给session添加错误的请求头
    session.headers["Authorization"] = "Bearer"+"error token"

    resp = session.request(
        method = api_info[api_name].method,url=api_info[api_name].url
    )

    assert resp.status_code != api_info[api_name].code


def test_sign_up_success(session):
    """
    测试：使用没注册账号，注册成功
    前置条件生成一个不会重复的账号
    执行动作：访问接口，并传参
    预期结果状态码为200
    """
    api_name="注册"
    email = f"{time.time():.2f}@q.c" #生成一个基于时间戳的账号，确保不重复  #len(str(time.time() ) )-->17位 所以报错，可保留2位小数
    password = email

    resp = session.request(api_info[api_name].method,api_info[api_name].url,json=dict(email=email,password=password) )

    assert resp.status_code == api_info[api_name].code,resp.text   #打印信息
    assert  resp.json().keys()== api_info[api_name].resp_body.keys()

def test_sign_up_fail(session):
    """
        测试：使用已注册账号，注册失败
        前置条件：选择一个已存在账号
        执行动作：访问接口，并传参
        预期结果状态码不等于200
        """
    api_name = "注册"
    email = user_info["email"]
    password = user_info["password"]

    resp = session.request(
        api_info[api_name].method,
        api_info[api_name].url,
        json=dict(email=email, password=password)
    )

    assert resp.status_code != api_info[api_name].code
