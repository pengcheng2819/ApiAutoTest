from datetime import datetime

import django
from django.db import models



class Api(models.Model):
    request_method_choice = (
        ('POST','POST'),
        ('GET','GET'),
        ('PUT','PUT'),
    )
    post_type_choice = (
        ('JSON','JSON'),
        ('FORM-DATA','FORM-DATA')
    )

    api_name = models.CharField(max_length=50)
    path = models.CharField(max_length=500)
    memo = models.CharField(max_length=100)
    request_method = models.CharField(choices=request_method_choice,max_length=10)
    params = models.CharField(max_length=10000,default={})
    cookies = models.CharField(max_length=10000, default={})
    base_head = models.CharField(max_length=1000,default={})
    post_type = models.CharField(choices=post_type_choice,max_length=50,default='JSON')
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
    request_method = models.CharField(choices=Api.request_method_choice, max_length=10,default='GET')
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

# class BaseCase(models.Model):


class Logic(models.Model):
    api = models.ForeignKey(Api,on_delete=models.CASCADE)



