import logging
from dataclasses import dataclass,field
from typing import Union, Text
from urllib.parse import urljoin

import requests
import requests_mock
from requests import PreparedRequest,Response


class APISession(requests.session):

    base_url=None
    logger = logging.getLogger("requests.seesion")
    __mock :requests_mock.Mocker

    def __init__(self,base_url=None):
        self.base_url = base_url
        self.logger.info("mock功能启动")
        super(APISession,self).__init__()

    def request(
            self,method:str,url:Union[str,bytes,Text],*args,**kwargs
    )->Response:
        url = urljoin(self.base_url,url)
        return super(APISession,self).request(method,url,*args,**kwargs)

    def send(self,request:PreparedRequest,**kwargs)->Response:
        self.logger.info(f"发送请求>>>接口地址 = {request.method}{request.url}")
        self.logger.debug(f"发送请求>>>请求头 = {request.headers}")
        self.logger.debug(f"发送请求>>>请求正文 = {request.body}")
        response = super(APISession,self).send(request,**kwargs)

        self.logger.info(f"接收响应<<< 状态码 = {response.status_code}")
        self.logger.debug(f"接收响应<<< 响应头 = {response.headers}")
        self.logger.debug(f"接收响应<<< 响应正文 = {response.text}")






@dataclass
class ApiInfo:
    method:str   #请求方式
    url:str     #请求地址
    params:dict= field(default_factory=lambda :{})
    body:dict =field(default_factory=lambda :{})
    code:int =200
    resp_body:dict=field(default_factory=lambda :{
        "code":0,
        "data":"",
        "msg":" "
    })




