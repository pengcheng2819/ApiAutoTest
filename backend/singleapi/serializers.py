# 作者      : pengcheng
# 创建时间  : 2020/7/21 15:11

from backend.singleapi.models import Api, ApiCase, OptionDict, ColumnTypeDict, OptionTypeDict
from rest_framework import serializers


class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Api
        fields = ['id', 'api_name', 'path', 'memo', 'request_method', 'params', 'cookies',
                  'base_head','post_type', 'base_body', 'base_expect', 'owner', 'create_time', 'update_time', 'status']


class ApiCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiCase
        fields = ['id', 'api', 'path', 'request_method', 'memo', 'params', 'cookies', 'case_name', 'head', 'body',
                  'expect', 'create_time', 'update_time', 'status']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionDict
        fields = ['option_type','title','value','widget','status']


class ColumnTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnTypeDict
        fields = ['title','value','status']


class OptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionTypeDict
        fields = ['typekey','column_type','title','status']