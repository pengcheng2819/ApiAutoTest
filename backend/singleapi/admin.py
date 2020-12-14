from django.contrib import admin
from django.contrib.admin import AdminSite

from backend.singleapi.models import Api,ApiCase,OptionDict,ColumnTypeDict,OptionTypeDict


@admin.register(OptionDict)
class OptionDictAdmin(admin.ModelAdmin):
    list_display = ('option_type','title','value','widget','status')    #显示字段
    list_per_page = 50      #每页多少条记录,默认显示100条
    list_filter = ('option_type','status')     #设置过滤器
    search_fields =('title', 'option_type__title', 'value') #搜索字段


@admin.register(ColumnTypeDict)
class ColumnTypeDictAdmin(admin.ModelAdmin):
    list_display = ('title','value','status')
    list_per_page = 50
    list_filter = ('status',)
    search_fields =('title', 'value',)

@admin.register(OptionTypeDict)
class OptionTypeDictAdmin(admin.ModelAdmin):
    list_display = ('typekey','column_type','title','status')
    list_per_page = 50
    list_filter = ('typekey','column_type','status')
    search_fields = ('title', 'column_type__title','typekey')

@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'api_name', 'path', 'memo', 'request_method', 'params', 'cookies',
                  'base_head','post_type', 'base_body','response_demo', 'expect_pass','expect_fail', 'owner', 'create_time', 'update_time', 'status')
    list_per_page = 50
    list_filter = ('request_method','status')
    search_fields = ('api_name', 'path', 'id','owner')
    date_hierarchy = 'create_time'  # 详细时间分层筛选

@admin.register(ApiCase)
class ApiCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'api', 'path', 'request_method', 'memo', 'params', 'cookies', 'case_name', 'head', 'body',
                  'expect', 'create_time', 'update_time', 'status')
    list_per_page = 50
    list_filter = ('request_method','create_time','status','api')
    search_fields = ('case_name', 'path', 'id','api__api_name')
    date_hierarchy = 'create_time'  # 详细时间分层筛选


