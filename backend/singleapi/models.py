
from django.db import models


class Api(models.Model):

    api_name = models.CharField(max_length=50)
    path = models.CharField(max_length=500)
    memo = models.CharField(max_length=100)
    request_method = models.CharField(max_length=10)
    params = models.CharField(max_length=10000,default={})
    cookies = models.CharField(max_length=10000, default={})
    base_head = models.CharField(max_length=1000,default={})
    post_type = models.CharField(max_length=50,default='JSON')
    base_body = models.CharField(max_length=10000,default={})
    response_demo = models.CharField(max_length=10000,default={})
    expect_pass = models.CharField(max_length=10000,default={"status":1})
    expect_fail = models.CharField(max_length=10000, default={"status":0})
    owner = models.CharField(max_length=50,default=None)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = '接口'

    def __str__(self):
        return self.api_name


class ApiCase(models.Model):
    case_name = models.CharField(max_length=100)
    api = models.ForeignKey(Api,on_delete=models.CASCADE)
    path = models.CharField(max_length=500,default='')
    request_method = models.CharField(max_length=10,default='GET')
    memo = models.CharField(max_length=100,default='')
    params = models.CharField(max_length=10000,default={})
    cookies = models.CharField(max_length=10000, default={})
    head = models.CharField(max_length=1000,blank=True)
    body = models.CharField(max_length=10000,blank=True)
    expect = models.CharField(max_length=10000)
    is_pass = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = '接口用例'

    def __str__(self):
        return self.case_name


class ColumnTypeDict(models.Model):
    # 字段类型字典表
    value = models.CharField(max_length=100, verbose_name='类型值', primary_key=True, unique=True)
    title = models.CharField(max_length=100,verbose_name='类型名称')
    status = models.IntegerField(default=1,verbose_name='状态')

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = '字段类型字典'

    def __str__(self):
        return self.title


class OptionTypeDict(models.Model):
    # 测试点选项类型字典表
    typekey = models.CharField(max_length=100,primary_key=True, unique=True,verbose_name='选项类型')
    column_type = models.ForeignKey('ColumnTypeDict',to_field='value',on_delete=models.CASCADE,verbose_name='所属字段类型')
    title = models.CharField(max_length=100,verbose_name='选项类型标题')
    status = models.IntegerField(default=1,verbose_name='状态')

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = '选项类型字典'

    def __str__(self):
        return self.title


class OptionDict(models.Model):
    # 测试点选项字典表
    widget_choice =(
        ('checkbox','复选框'),
        ('input','输入框'),
        ('select','下拉框'),
        ('selects', '多选下拉框'),
        ('select-input', '下拉框+输入框'),
        ('select-input-input', '下拉框+输入框+输入框'),
        ('input-input', '输入框+输入框'),
        ('doubleinput','区间输入框'),
        ('null','无需控件')
    )
    option_type = models.ForeignKey('OptionTypeDict',on_delete=models.CASCADE,to_field='typekey',verbose_name='选项类型')
    title = models.CharField(max_length=100,verbose_name='选项标题')
    value = models.CharField(max_length=20, verbose_name='选项值',primary_key=True,unique=True,default='')
    widget = models.CharField(max_length=100,choices=widget_choice,default=('输入框','input'),verbose_name='所需控件')
    status = models.IntegerField(default=1,verbose_name='状态')

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = '选项字典'

    def __str__(self):
        return self.title

