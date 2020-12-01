# 作者      : pengcheng
# 创建时间  : 2020/11/19 16:01


from django.db.models import Q
from rest_framework.views import APIView

from backend.singleapi.serializers import OptionSerializer,ColumnTypeSerializer,OptionTypeSerializer
from backend.singleapi.models import ColumnTypeDict,OptionTypeDict,OptionDict
from backend.singleapi.tools import try_result


class ColumnTypeList(APIView):
    @try_result('获取字段类型列表')
    def get(self, request):
        column_type_list = ColumnTypeDict.objects.filter(~Q(status=0))
        serializer = ColumnTypeSerializer(column_type_list, many=True)
        return serializer.data


class OptionTypeList(APIView):
    @try_result('获取选项类型列表')
    def get(self, request):
        option_type_list = OptionTypeDict.objects.filter(~Q(status=0))
        serializer = OptionTypeSerializer(option_type_list, many=True)
        return serializer.data


class OptionList(APIView):
    @try_result('获取选项列表')
    def get(self, request):
        option_list = OptionDict.objects.filter(~Q(status=0))
        serializer = OptionSerializer(option_list, many=True)
        return serializer.data
