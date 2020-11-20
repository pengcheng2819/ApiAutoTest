import subprocess

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.utils import json

from backend.singleapi.serializers import ApiCaseSerializer, ApiSerializer
from rest_framework.views import APIView
from backend.singleapi.models import Api, ApiCase
import requests


# Api

class ApiList(APIView):
    def get(self, request):
        try:
            apilist = Api.objects.filter(~Q(status=0))
            serializer = ApiSerializer(apilist, many=True)
            result = {
                'msg': "获取接口列表成功！",
                'data': serializer.data,
                'status': 1
            }

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {
                'msg': "获取接口列表失败！" + str(e),
                'status': 0
            }
            return Response(result)


class QueryApiList(APIView):
    def post(self, request):
        try:
            text = request.data['text']
            method = request.data['method']
            apilist = Api.objects.filter(~Q(status=0))
            if (method):
                apilist = apilist.filter(request_method=method)
            if (text):
                if (text.isdigit()):
                    apilist = apilist.filter(id=int(text))
                else:
                    apilist = apilist.filter(
                        Q(api_name__icontains=text) | Q(path__icontains=text) | Q(memo__icontains=text))
            serializer = ApiSerializer(apilist, many=True)
            result = {
                'msg': "查询接口列表成功！",
                'data': serializer.data,
                'status': 1
            }
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {
                'msg': "查询接口列表失败！" + str(e),
                'status': 0
            }
            return Response(result)


class ApiDetail(APIView):
    def get(self, request, pk):
        api = get_object_or_404(Api, pk=pk)
        if api and api.status:
            serializer = ApiSerializer(api)
            result = {"msg": "id为【%d】的接口查询成功！" % pk, "status": 1, "data": serializer.data}
            return Response(result)
        result = {"msg": "id为【%d】的接口不存在或已删除！" % pk, "status": 0}
        return Response(result)


class ApiAdd(generics.CreateAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer


class ApiUpdate(APIView):
    def post(self, request):
        api = get_object_or_404(Api, pk=request.data['id'])
        serializer = ApiSerializer(api, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiDelete(APIView):
    def post(self, request):
        try:
            apilist = Api.objects.filter(pk__in=request.data['id'])
            apicaselist = ApiCase.objects.filter(api__in=apilist)
            for api in apilist:
                api.delete()
                # api.status = 0
                # api.save()
                # 删除相关的case
                delete_apicase(apicaselist)
            result = {
                'msg': "删除成功！",
                'data': [{'接口名称': api.api_name, '接口id': api.id} for api in apilist],
                'status': 1
            }
        except Exception as e:
            result = {
                'msg': "删除失败，错误信息为：" + str(e),
                'status': 0
            }
            return Response(result, status=200)
        return Response(result, status=200)



# ApiCase
class ApiCaseList(generics.ListAPIView):
    def get(self, request):
        try:
            queryset = ApiCase.objects.filter(~Q(status=0))
            serializer = ApiCaseSerializer(queryset, many=True)
            result = {
                'msg': "获取接口列表成功！",
                'data': serializer.data,
                'status': 1
            }

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {
                'msg': "获取接口列表失败！" + str(e),
                'status': 0
            }
            return Response(result)


class QueryCaseList(APIView):
    def post(self, request):
        try:
            text = request.data['text']
            api = request.data['api']
            caselist = ApiCase.objects.filter(~Q(status=0))
            if (api):
                print(api)
                caselist = caselist.filter(api_id__in=api)
            if (text):
                if (text.isdigit()):
                    caselist = caselist.filter(id=int(text))
                else:
                    caselist = caselist.filter(
                        Q(case_name__icontains=text) | Q(body__icontains=text) | Q(expect__icontains=text))
            print(caselist)
            serializer = ApiCaseSerializer(caselist, many=True)
            result = {
                'msg': "查询接口列表成功！",
                'data': serializer.data,
                'status': 1
            }
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {
                'msg': "查询接口列表失败！" + str(e),
                'status': 0
            }
            return Response(result)


class ApiCaseUpdate(APIView):
    def post(self, request):
        apicase = get_object_or_404(ApiCase, pk=request.data['id'])
        serializer = ApiCaseSerializer(apicase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiCaseAdd(generics.CreateAPIView):
    queryset = ApiCase.objects.all()
    serializer_class = ApiCaseSerializer


class ApiCaseDetail(APIView):
    def get(self, request, pk):
        apicase = get_object_or_404(ApiCase, pk=pk)
        if apicase and apicase.status:
            serializer = ApiCaseSerializer(apicase)
            result = {"msg": "id为【%d】的Case查询成功！" % pk, "status": 1, "data": serializer.data}
            return Response(result)
        reslut = {"msg": "id为【%d】的Case不存在或已删除！" % pk, "status": 0},
        return Response(reslut)


class ApiCaseDelete(APIView):
    def post(self, request):
        try:
            apicaselist = ApiCase.objects.filter(pk__in=request.data['id'])
            delete_apicase(apicaselist)
            result = {
                'msg': "删除成功！",
                'data': [case.case_name for case in apicaselist],
                'status': 1
            }
        except Exception as e:
            result = {
                'msg': "删除失败，错误信息为：" + str(e),
                'status': 0
            }
            return Response(result, status=200)
        return Response(result, status=200)


def delete_apicase(apicaselist):
    for apicase in apicaselist:
        apicase.delete()
        # apicase.status = 0
        # apicase.save()


# 执行Case
class TestRunCase(APIView):

    def post(self, request):
        apicase = request.data
        try:
            if apicase['request_method'] == 'POST':
                respones = requests.post(url=apicase['path'], data=apicase['body'], params=apicase['params'],
                                         headers=apicase['head'], cookies=apicase['cookies'])
                result = respones.text
            elif apicase['request_method'] == 'GET':
                respones = requests.get(url='http://192.168.156.124:8000' + apicase['path'], data=apicase['body'],
                                        params=apicase['params'])
                result = respones.text
        except Exception as e:
            result = {"msg": "接口请求失败！", "status": 0}
        return Response(result)



