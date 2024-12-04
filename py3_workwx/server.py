#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import timedelta
from typing import Callable, Any, Union

import diskcache
import redis
import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from py3_response_handler.requests import ResponseHandler


class ResponseHandler(ResponseHandler):
    def json_errcode_0(self, response: requests.Response = None, status_code: int = 200):
        json_addict = self.json_to_addict(response, status_code)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "errcode": {
                    "oneOf": [
                        {"type": "integer", "const": 0},
                        {"type": "string", "const": "0"},
                    ]
                }
            },
            "required": ["errcode"],
        }).is_valid(json_addict):
            return json_addict.data
        return None


class Server:
    """
    @see https://developer.work.weixin.qq.com/document/path/90664
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com/",
            corpid: str = "",
            corpsecret: str = "",
            agentid: Union[int, str] = "",
            cache_instance: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None,
    ):
        self._base_url: str = base_url
        self._corpid: str = corpid
        self._corpsecret: str = corpsecret
        self._agentid: Union[int, str] = agentid
        self._cache_instance: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = cache_instance
        self._access_token: str = ""
        self._response_handler: ResponseHandler = ResponseHandler()

    @property
    def agentid(self) -> Union[int, str]:
        return self._agentid

    def get_api_domain_ip(
            self,
            response_handler_callable: Callable = None,
            method: str = "GET",
            url: str = "/cgi-bin/get_api_domain_ip",
            params: dict = None,
            *args,
            **kwargs
    ):
        if self._base_url.endswith("/"):
            self._base_url = self._base_url[:-1]
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self._base_url}{url}"
        params = Dict({})
        params.setdefault("access_token", self._access_token)
        response = requests.request(
            method=method,
            url=url,
            params=params.to_dict(),
            *args,
            **kwargs
        )
        if isinstance(response_handler_callable, Callable):
            return response_handler_callable(response)
        json_addict = self._response_handler.json_to_addict(response, 200)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "ip_list": {"type": "array", "minItem": 1},
            },
            "required": ["ip_list"]
        }).is_valid(json_addict):
            return json_addict.ip_list
        return None

    def gettoken(
            self,
            response_handler_callable: Callable = None,
            expire: Union[float, int, timedelta] = None,
            method: str = "GET",
            url: str = "/cgi-bin/gettoken",
            params: dict = None,
            *args,
            **kwargs
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91039
        :param response_handler_callable: response handler callable
        :param expire: cache expire in seconds
        :param method: requests.request method
        :param url: requests.request url
        :param params: requests.request params
        :param args: requests.request args
        :param kwargs: requests.request kwargs
        :return:
        """
        if isinstance(self._cache_instance, Union[diskcache.Cache, redis.Redis, redis.StrictRedis]):
            self._access_token = self._cache_instance.get(f"py3_workwx_server_access_token_{self._agentid}")
        api_domain_ip_list = self.get_api_domain_ip(access_token=self._access_token)
        if isinstance(api_domain_ip_list, list) and len(api_domain_ip_list):
            return self
        if self._base_url.endswith("/"):
            self._base_url = self._base_url[:-1]
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self._base_url}{url}"
        params = Dict(params)
        params.setdefault("corpid", self._corpid)
        params.setdefault("corpsecret", self._corpsecret)
        response = requests.request(
            method=method,
            url=url,
            params=params.to_dict(),
            *args,
            **kwargs
        )
        if isinstance(response_handler_callable, Callable):
            response_handler_callable(response)
            return self
        json_addict = self._response_handler.json_errcode_0(response)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "access_token": {"type": "string", "minLength": 1},
            },
            "required": ["access_token"]
        }).is_valid(json_addict):
            self._access_token = json_addict.get("access_token", None)
            if isinstance(self._cache_instance, diskcache.Cache):
                return self._cache_instance.set(
                    key=f"py3_workwx_server_access_token_{self._agentid}",
                    value=self._access_token,
                    expire=expire or timedelta(seconds=7100).total_seconds()
                )
            if isinstance(self._cache_instance, (redis.Redis, redis.StrictRedis)):
                self._cache_instance.setex(
                    name=f"py3_workwx_server_access_token_{self._agentid}",
                    value=self._access_token,
                    time=expire or timedelta(seconds=7100),
                )
        return self
