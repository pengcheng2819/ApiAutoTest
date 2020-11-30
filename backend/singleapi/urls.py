# 作者      : pengcheng
# 创建时间  : 2020/7/1 18:24

from django.urls import path, include

from backend.singleapi.views import views, dictviews,caseviews

urlpatterns = [
    path('list/', views.ApiList.as_view(), name='apilist'),
    path('queryapilist/', views.QueryApiList.as_view(), name='queryapilist'),
    path('updateapi/', views.ApiUpdate.as_view(), name='updateapi'),
    path('newapi/', views.ApiAdd.as_view(), name='newapi'),
    path('delapi/', views.ApiDelete.as_view(), name='delapi'),
    path('<int:pk>/apidetail/', views.ApiDetail.as_view(), name='apidetail'),

    path('newcase/', views.ApiCaseAdd.as_view(), name='newapicase'),
    path('caselist/', views.ApiCaseList.as_view(), name='caselist'),
    path('querycaselist/', views.QueryCaseList.as_view(), name='queryapilist'),
    path('updatecase/', views.ApiCaseUpdate.as_view(), name='updateapicase'),
    path('delapicase/', views.ApiCaseDelete.as_view(), name='delapicase'),
    path('<int:pk>/casedetail/', views.ApiCaseDetail.as_view(), name='editcase'),
    path('testruncase/', views.TestRunCase.as_view(), name='runcase'),

    path('columntypelist/', dictviews.ColumnTypeList.as_view(), name='columntypelist'),
    path('optiontypelist/', dictviews.OptionTypeList.as_view(), name='optiontypelist'),
    path('optionlist/', dictviews.OptionList.as_view(), name='optionlist'),

    path('createcase/', caseviews.CreateCase.as_view(), name='createcase'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
