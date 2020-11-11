# -*- coding: UTF-8 -*-
# 时间：2020/8/25 21:00
import json
import requests
from django.shortcuts import get_object_or_404
from backend.singleapi.models import ApiCase


class RunRequest():
    def test_request(self,caselist):
        apicase  = get_object_or_404(ApiCase, pk=caselist)
        respones = requests.get(url='http://192.168.0.107:8080'+apicase['path'],
                                params=None,headers=None,cookies=None)
        assert respones.text == '0'


    def post(self,url,data=None,params=None,cookies=None,headers=None):
        respones = requests.post(url=url,params=params,headers=headers,cookies=cookies)
        return respones

    def get(self):
        pass




