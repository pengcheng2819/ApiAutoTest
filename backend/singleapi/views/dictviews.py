# 作者      : pengcheng
# 创建时间  : 2020/11/19 16:01 

import subprocess

from django.db.models import Q
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.singleapi.serializers import OptionSerializer,ColumnTypeSerializer,OptionTypeSerializer
from backend.singleapi.models import ColumnTypeDict,OptionTypeDict,OptionDict


class ColumnTypeList(APIView):
    def get(self, request):
        try:
            ColumnTypelist = ColumnTypeDict.objects.filter(~Q(status=0))
            serializer = ColumnTypeSerializer(ColumnTypelist, many=True)
            result = {
                'msg': "获取字段类型列表成功！",
                'data': serializer.data,
                'status': 1
            }

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {
                'msg': "获取字段类型列表失败！" + str(e),
                'status': 0
            }
            return Response(result)


class OptionTypeList(APIView):
    def get(self, request):
        try:
            OptionTypelist = OptionTypeDict.objects.filter(~Q(status=0))
            serializer = OptionTypeSerializer(OptionTypelist, many=True)
            result = {
                'msg': "获取选项类型列表成功！",
                'data': serializer.data,
                'status': 1
            }

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {
                'msg': "获取选项类型列表失败！" + str(e),
                'status': 0
            }
            return Response(result)


class OptionList(APIView):
    def get(self, request):
        try:
            Optionlist = OptionDict.objects.filter(~Q(status=0))
            serializer = OptionSerializer(Optionlist, many=True)
            result = {
                'msg': "获取选项列表成功！",
                'data': serializer.data,
                'status': 1
            }

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {
                'msg': "获取选项列表失败！" + str(e),
                'status': 0
            }
            return Response(result)