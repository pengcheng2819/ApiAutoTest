from datetime import datetime

import django
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
    base_expect = models.CharField(max_length=10000,default={})
    owner = models.CharField(max_length=50,default=None)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)


    class Meta:
        ordering = ['-pk']

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
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.case_name


class Option(models.Model):
    type_choice = (
        ('tt','method'),
        ('字段值类型','valuetype'),
        ('待测条件','condioptions'),
        ('发送数据类型', 'posttype'),
    )
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    type = models.CharField(choices=type_choice,max_length=20)
    status = models.IntegerField(default=1)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.title

class Logic(models.Model):
    api = models.ForeignKey(Api,on_delete=models.CASCADE)



