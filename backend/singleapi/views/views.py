import subprocess

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response


from backend.singleapi.serializers import ApiCaseSerializer, ApiSerializer
from rest_framework.views import APIView
from backend.singleapi.models import Api, ApiCase
import requests
from backend.singleapi.tools import try_result


# Api

class ApiList(APIView):
    @try_result('获取接口列表')
    def get(self, request):
        api_list = Api.objects.filter(~Q(status=0))
        serializer = ApiSerializer(api_list, many=True)
        return serializer.data


class QueryApiList(APIView):
    @try_result('查询接口列表')
    def post(self, request):
        text = request.data['text']
        method = request.data['method']
        api_list = Api.objects.filter(~Q(status=0))
        if method:
            api_list = api_list.filter(request_method=method)
        if text:
            if text.isdigit():
                api_list = api_list.filter(id=int(text))
            else:
                api_list = api_list.filter(
                    Q(api_name__icontains=text) | Q(path__icontains=text) | Q(memo__icontains=text))
        serializer = ApiSerializer(api_list, many=True)
        return serializer.data


class ApiDetail(APIView):
    @try_result('接口详情查看')
    def get(self, request, pk):
        api = get_object_or_404(Api, pk=pk)
        if api and api.status:
            serializer = ApiSerializer(api)
            return serializer.data


class ApiAdd(generics.CreateAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer


class ApiUpdate(APIView):
    @try_result('接口更新')
    def post(self, request):
        api = get_object_or_404(Api, pk=request.data['id'])
        serializer = ApiSerializer(api, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return request.data['id']
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiDelete(APIView):
    @try_result('接口删除')
    def post(self, request):
        api_list = Api.objects.filter(pk__in=request.data['id'])
        api_case_list = ApiCase.objects.filter(api__in=api_list)
        for api in api_list:
            # api.delete()      #物理删除
            api.status = 0      #逻辑删除
            api.save()
            # 删除相关的case
            delete_apicase(api_case_list)
        return [{'接口名称': api.api_name, '接口id': api.id} for api in api_list]


# ApiCase
class ApiCaseList(generics.ListAPIView):
    @try_result('获取接口测试用例列表')
    def get(self, request):
        queryset = ApiCase.objects.filter(~Q(status=0))
        serializer = ApiCaseSerializer(queryset, many=True)
        return serializer.data


class QueryCaseList(APIView):
    @try_result('查询接口测试用例列表')
    def post(self, request):
        text = request.data['text']
        api = request.data['api']
        case_list = ApiCase.objects.filter(~Q(status=0))
        if api:
            case_list = case_list.filter(api_id__in=api)
        if text:
            if text.isdigit():
                case_list = case_list.filter(id=int(text))
            else:
                case_list = case_list.filter(
                    Q(case_name__icontains=text) | Q(body__icontains=text) | Q(expect__icontains=text))
        print(case_list)
        serializer = ApiCaseSerializer(case_list, many=True)
        return serializer.data


class ApiCaseUpdate(APIView):
    @try_result('更新接口测试用例')
    def post(self, request):
        api_case = get_object_or_404(ApiCase, pk=request.data['id'])
        serializer = ApiCaseSerializer(api_case, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiCaseAdd(generics.CreateAPIView):
    queryset = ApiCase.objects.all()
    serializer_class = ApiCaseSerializer


class ApiCaseDetail(APIView):
    @try_result('查看接口测试用例详情')
    def get(self, request, pk):
        api_case = get_object_or_404(ApiCase, pk=pk)
        if api_case and api_case.status:
            serializer = ApiCaseSerializer(api_case)
            return serializer.data


class ApiCaseDelete(APIView):
    @try_result('删除接口测试用例')
    def post(self, request):
        api_case_list = ApiCase.objects.filter(pk__in=request.data['id'])
        delete_apicase(api_case_list)
        return [case.case_name for case in api_case_list]


def delete_apicase(apicaselist):
    for api_case in apicaselist:
        # apicase.delete()      #物理删除
        api_case.status = 0      #逻辑删除
        api_case.save()


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



