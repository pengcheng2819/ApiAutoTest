# 作者      : pengcheng
# 创建时间  : 2020/11/25 13:46
import exrex
from django.db.models import Q
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
import json


from backend.singleapi.models import Api, ApiCase



class CreateCase(APIView):

    regular = {
        'email':'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'domain': '[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(/.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+/.?',
        'url':'^(http|https):\/\/[A-Za-z0-9]+\.[A-Za-z0-9]+[\/=\?%\-&_~`@[\]\':+!]*([^<>\"\"])*$',
        'moblephone':'^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$',
        'telphone':'((\(0\d{2,3}\))|(0\d{2,3}[-]?))\d{7,8} ',
        'id':'(^\d{15}|\d{18}$)|(^([0-9]){7,18}(x|X)?$)',
        'userid':'^[a-zA-Z][a-zA-Z0-9_]{4,15}$',
        'chinese':'[\u4e00-\u9fa5]',
        'qq':'[1-9][0-9]{4,12}',
        'emailcode':'[1-9]\d{5}(?!\d)',
        'ip':'((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))',
}

    def post(self, request):
        try:
            apiid = request.data['id']
            apiobj = Api.objects.get(id=apiid)
            self.need_create(apiobj.params)
            self.need_create(apiobj.base_body)

            result = {
                'msg': "自动生成case成功！",
                'status': 1
            }

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {
                'msg': "自动生成case失败！" + str(e),
                'status': 0
            }
            return Response(result)


    def need_create(self,obj):
        if len(obj) > 0:
            paramlist = json.loads(obj)
            for param in paramlist:
                # print(param)
                if param['type']=='string':
                    # 如果字段值是限定选项，那么优先级最高，仅生成可选的值
                    if 'string-select' in param['condition']:
                        paramvaluelist = self.string_select(param['conditionValue']['string-select']['input'][0])
                        print(paramvaluelist)
                        # return paramvaluelist
                    lengthlist = []
                    # 如果有字符串长度测试点，则计算出需要测试的长度case
                    if 'string-length' in param['condition']:
                        lengthlist = self.string_length(param['conditionValue']['string-length'])
                    randomvalue = ''
                    if 'string-random' in param['condition']:
                        # 有长度限制时才执行
                        if lengthlist:
                            # 需要加动态字符串时，需要提前减去动态字符串长度，减完后长度小于0的case直接删掉
                            for length in lengthlist:
                                if length['value'] - 8 > 0:
                                    length['value'] = length['value'] - 8
                                else:
                                    lengthlist.pop(length)
                        randomvalue = '{{'+param['conditionValue']['string-random']['value']+'}}'
                    if 'string-regular' in param['condition']:
                        regularlist = self.string_regular(param['conditionValue']['string-regular'])
                        print(regularlist)






                    # print(lengthlist)

    # 限定选项处理,一个正向,一个反向
    def string_select(self,select):
        choicelist = select.split(',')
        choiceobj = []
        for choice in choicelist:
            choiceobj.append({'titile':'选值'+choice,'value':choice,'ispass':True})
            discontent = exrex.getone('[^' + choice + ']{'+str(len(choice))+'}')
            choiceobj.append({'titile':'选值'+discontent,'value':discontent,'ispass':False})
        return choiceobj

    # 生成需要测试的字符长度
    def string_length(self,length):
        input = length['input']
        if len(input)==2:
            return [
                {'title':'小于规定长度','value':int(input[0])-1,'ispass':False},
                {'title': '大于规定长度', 'value': int(input[1]) + 1,'ispass':False},
                {'title': '规定长度最小值', 'value': int(input[0]),'ispass':True},
                {'title': '规定长度最大值', 'value': int(input[1]),'ispass':True},
                {'title': '规定长度中间', 'value': int(input[0])+int((int(input[1])-int(input[0]))/2),'ispass':True},
                    ]
        elif len(input)==1:
            if length['value'] == 'lt':
                return [
                    {'title': '大于规定长度', 'value': int(input[0])+1, 'ispass': False},
                    {'title': '最大规定长度', 'value': int(input[0]), 'ispass': True},
                    {'title': '最小规定长度', 'value': 1, 'ispass': True},
                    {'title': '规定长度中间值', 'value': int(int(input[0])/2), 'ispass': True},
                ]
            if length['value'] == 'gt':
                return [
                    {'title': '小于规定长度', 'value': int(input[0])-1, 'ispass': False},
                    {'title': '最小规定长度', 'value': int(input[0]), 'ispass': True},
                    {'title': '规定长度中间值', 'value': int(input[0])+int(int(input[0])/2), 'ispass': True},
                ]
            if length['value'] == 'eq':
                return [
                    {'title': '规定长度-1', 'value': int(input[0])-1, 'ispass': False},
                    {'title':'规定长度+1','value':int(input[0])+1,'ispass':False},
                    {'title': '规定长度', 'value': int(input[0]), 'ispass': True},
                ]

    def string_regular(self,regular):
        regularobj = []
        if regular['value'] == 'regular':
            for i in range(5):
                value = exrex.getone(regular['input'][0])
                regularobj.append({'title':'值'+value,'value':value,'ispass':True})
        else:
            for i in range(5):
                value = exrex.getone(self.regular[regular['value']])
                regularobj.append({'title':'值'+value,'value':value,'ispass':True})
        return regularobj



    def splicing_value(self,str):
        pass

    def string_regular_regular(self,input):
        obj = {
            'success':[],
            'fail':[]
        }
        obj['success'] = exrex.getone('['+input[0]+']')
        obj['failed'] = exrex.getone('[^' + input[0] + ']')

    def string_special(self,input):
        return exrex.getone('['+input[0]+']{15}')

    # def string_special_notinclude(self,input):
    #     return exrex.getone('[^'+input[0]+']{15}')

