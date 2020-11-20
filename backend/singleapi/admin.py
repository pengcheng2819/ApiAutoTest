from django.contrib import admin
from backend.singleapi.models import Api,ApiCase,OptionDict,ColumnTypeDict,OptionTypeDict


@admin.register(OptionDict)
class OptionDictAdmin(admin.ModelAdmin):
    list_display = ('id','option_type','title','widget','status')

@admin.register(ColumnTypeDict)
class ColumnTypeDictAdmin(admin.ModelAdmin):
    list_display = ('id','title','value','status')

@admin.register(OptionTypeDict)
class OptionTypeDictAdmin(admin.ModelAdmin):
    list_display = ('id','column_type','title','value','status')

@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'api_name', 'path', 'memo', 'request_method', 'params', 'cookies',
                  'base_head','post_type', 'base_body', 'base_expect', 'owner', 'create_time', 'update_time', 'status')

@admin.register(ApiCase)
class ApiCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'api', 'path', 'request_method', 'memo', 'params', 'cookies', 'case_name', 'head', 'body',
                  'expect', 'create_time', 'update_time', 'status')