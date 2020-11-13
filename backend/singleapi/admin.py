from django.contrib import admin
from backend.singleapi.models import Api,ApiCase,Option


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id','title','value','type','status')

@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'api_name', 'path', 'memo', 'request_method', 'params', 'cookies',
                  'base_head','post_type', 'base_body', 'base_expect', 'owner', 'create_time', 'update_time', 'status')

@admin.register(ApiCase)
class ApiCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'api', 'path', 'request_method', 'memo', 'params', 'cookies', 'case_name', 'head', 'body',
                  'expect', 'create_time', 'update_time', 'status')