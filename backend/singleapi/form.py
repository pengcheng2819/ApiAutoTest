# 作者      : pengcheng
# 创建时间  : 2020/7/2 14:09 

from django import forms
from backend.singleapi.models import Api,ApiCase

class NewApiForm(forms.ModelForm):
    request_method_choice = (
        ('POST','POST'),
        ('GET','GET'),
        ('PUT', 'PUT'),
    )
    api_name = forms.CharField(max_length=50,widget=forms.TextInput(
        attrs={'placeholder':'请输入接口名称','size':'40'}
    ),label='接口名称：')
    memo = forms.CharField(widget=forms.Textarea(
        attrs={'rows':2,'placeholder':'请输入接口描述'}
    ),max_length=100,label='接口文档描述：')
    path = forms.CharField(max_length=500,widget=forms.Textarea(
        attrs={'rows':1,'placeholder':'请输入接口路径'}
    ),label='接口路径：')

    request_method = forms.ChoiceField(choices=request_method_choice,label='请求方法：')
    base_head = forms.CharField(max_length=1000,widget=forms.Textarea(
        attrs={'rows':5,'placeholder':'请输入接口基础头部'}
    ),label='请求Head：')
    base_body = forms.CharField(max_length=10000,widget=forms.Textarea(
        attrs={'rows':5,'placeholder':'请输入接口基础请求体'}
    ),label='请求Body：')
    base_expect = forms.CharField(max_length=10000,widget=forms.Textarea(
        attrs={'rows':5,'placeholder':'请输入接口基础预期结果'}
    ),label='预期结果：')


    class Meta:
        model = Api
        fields = ['api_name','memo','path','request_method','base_head','base_body','base_expect']


class NewApiCaseForm(forms.ModelForm):

    case_name = forms.CharField(max_length=50,widget=forms.Textarea(
        attrs={'rows':1,'placeholder':'请输入用例名称'}
    ),label='用例名称：')

    head = forms.CharField(max_length=1000,widget=forms.Textarea(
        attrs={'rows':5,'placeholder':'请输入补充head'}
    ),label='补充head:',required=False,initial={})
    body = forms.CharField(max_length=10000,widget=forms.Textarea(
        attrs={'rows':5,'placeholder':'请输入补充body'}
    ),label='补充body:',required=False,initial={'headline': 'Initial headline'})
    expect = forms.CharField(max_length=10000,widget=forms.Textarea(
        attrs={'rows':5,'placeholder':'请输入预期结果'}
    ),label='预期结果:')

    class Meta:
        model = ApiCase
        fields = ['case_name','head','body','expect']