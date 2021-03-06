# 作者      : pengcheng
# 创建时间  : 2020/11/25 13:46
import exrex
from rest_framework.views import APIView
import json
import random

from backend.singleapi.models import Api, ApiCase
from backend.singleapi.tools import try_result


class CreateCase(APIView):
    regular = {
        'email': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'domain': '[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(/.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+/.?',
        'url': '^(http|https):\/\/[A-Za-z0-9]+\.[A-Za-z0-9]+[\/=\?%\-&_~`@[\]\':+!]*([^<>\"\"])*$',
        'moblephone': '^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$',
        'telphone': '((\(0\d{2,3}\))|(0\d{2,3}[-]?))\d{7,8} ',
        'id': '(^\d{15}|\d{18}$)|(^([0-9]){7,18}(x|X)?$)',
        'userid': '^[a-zA-Z][a-zA-Z0-9_]{4,15}$',
        'chinese': '[\u4e00-\u9fa5]',
        'qq': '[1-9][0-9]{4,12}',
        'emailcode': '[1-9]\d{5}(?!\d)',
        'ip': '((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))',
        'all': '[a-zA-Z0-9\u4e00-\u4fa5~!@#$%^&*()_+`\-={}|\[\]\\:"<>?;\',\./]'
    }

    randomlength = {
        'date':10,
        'time':5,
        'timestamp':11,
        'datetime':16,
    }

    @try_result('自动生成CASE')
    def post(self, request):
        apiid = request.data['id']
        istest = request.data['istest']
        apiobj = Api.objects.get(id=apiid)
        paramslist = self.need_create(apiobj.params)    #判断是否
        bodylist = self.need_create(apiobj.base_body)
        paramtrue = self.get_true(paramslist)   #获取所有正向的用例
        bodytrue = self.get_true(bodylist)
        if istest:  #判断是否为测试生成
            param = self.get_one(paramtrue)
            body = self.get_one(bodytrue)
            ids = self.insert_case(apiobj, [param], [body], paramtrue, bodytrue)
            return {'ids':ids}
        else:
            apicaselist = ApiCase.objects.filter(api_id=apiid,status=2)
            self.del_case(apicaselist)
            params = self.get_all(paramslist,paramtrue)
            bodys = self.get_all(bodylist, bodytrue)
            ids = self.insert_case(apiobj,params,bodys,paramtrue,bodytrue)
            return {'ids':ids}

    # 判断是否需要自动生成case
    def need_create(self, obj):
        '''
        obj : 需要生成case的对象
        '''
        if len(obj) > 0:
            paramlist = json.loads(obj)
            paramobj = {}
            for param in paramlist:
                if param['type'] == 'string':
                    lengthlist = []
                    # 如果有字符串长度测试点，则计算出需要测试的长度case
                    if 'string-length' in param['condition']:
                        lengthlist = self.string_length(param['conditionValue']['string-length'])
                    randomvalue = ''
                    if 'string-random' in param['condition']:
                        placeholder = param['conditionValue']['string-random']['input'][0]
                        randomvalue = '{{' + placeholder + '}}'
                        # 有长度限制时才执行
                        if lengthlist:
                            # 需要加动态字符串时，需要提前减去动态字符串长度，减完后长度小于0的case直接删掉
                            for length in lengthlist:
                                if length['value'] - self.randomlength[placeholder] > 0:
                                    length['value'] = length['value'] - self.randomlength[placeholder]       #减去动态字符所需的长度
                                else:
                                    lengthlist.pop(length)
                    # 如果字段值是限定选项，那么优先级最高，仅生成可选的值
                    if 'string-select' in param['condition']:
                        selectlist = self.string_select(param['conditionValue']['string-select']['input'][0],
                                                        randomvalue)
                        paramobj[param['paramname']] = selectlist
                        continue
                    # 正则处理
                    if 'string-regular' in param['condition']:
                        regularlist = self.string_regular(param['conditionValue']['string-regular'], randomvalue)
                        paramobj[param['paramname']] = regularlist
                        continue
                    # 特殊字符处理
                    if 'string-special' in param['condition']:
                        speciallist = self.string_special(param['conditionValue']['string-special'], lengthlist,
                                                          randomvalue)
                        paramobj[param['paramname']] = speciallist
                        continue
                    paramobj[param['paramname']] = self.string_all(lengthlist,randomvalue)
                elif param['type'] == 'int':
                    pass
            return paramobj

    # 限定选项处理,一个正向,一个反向
    def string_select(self, select, randomvalue):
        '''
        select : 输入的可选项字符串
        randomvalue : 动态字符串
        '''
        choicelist = select.split(',')
        choiceobj = []
        for choice in choicelist:
            if choice:
                choiceobj.append({'title': '符合可选值', 'value': choice + randomvalue, 'ispass': True})
                discontent = exrex.getone('[^' + choice + ']{' + str(len(choice)) + '}')
                choiceobj.append({'title': '不符合可选值', 'value': discontent + randomvalue, 'ispass': False})
        return choiceobj

    # 生成需要测试的字符长度
    def string_length(self, length):
        '''
        length : 输入的长度取值范围
        '''
        input = length['input']
        if len(input) == 2:
            return [
                {'title': '小于规定长度', 'value': int(input[0]) - 1, 'ispass': False},
                {'title': '大于规定长度', 'value': int(input[1]) + 1, 'ispass': False},
                {'title': '规定长度最小值', 'value': int(input[0]), 'ispass': True},
                {'title': '规定长度最大值', 'value': int(input[1]), 'ispass': True},
                {'title': '规定长度中间', 'value': int(input[0]) + int((int(input[1]) - int(input[0])) / 2), 'ispass': True},
            ]
        elif len(input) == 1:
            if length['value'] == 'lt':
                return [
                    {'title': '大于规定长度', 'value': int(input[0]) + 1, 'ispass': False},
                    {'title': '最大规定长度', 'value': int(input[0]), 'ispass': True},
                    {'title': '最小规定长度', 'value': 1, 'ispass': True},
                    {'title': '规定长度中间值', 'value': int(int(input[0]) / 2), 'ispass': True},
                ]
            if length['value'] == 'gt':
                return [
                    {'title': '小于规定长度', 'value': int(input[0]) - 1, 'ispass': False},
                    {'title': '最小规定长度', 'value': int(input[0]), 'ispass': True},
                    {'title': '规定长度中间值', 'value': int(input[0]) + int(int(input[0]) / 2), 'ispass': True},
                ]
            if length['value'] == 'eq':
                return [
                    {'title': '规定长度-1', 'value': int(input[0]) - 1, 'ispass': False},
                    {'title': '规定长度+1', 'value': int(input[0]) + 1, 'ispass': False},
                    {'title': '规定长度', 'value': int(input[0]), 'ispass': True},
                ]

    # 正则处理,没有反向,随机生成5个正向值
    def string_regular(self, regular, randomvalue):
        '''
        regular : 需要处理的正则
        randomvalue : 动态字符串
        '''
        regularobj = []
        if regular['value'] == 'regular':
            for i in range(5):
                value = exrex.getone(regular['input'][0])
                regularobj.append({'title': '值' + value, 'value': value + randomvalue, 'ispass': True})
        else:
            for i in range(5):
                value = exrex.getone(self.regular[regular['value']])
                regularobj.append({'title': '值' + value, 'value': value + randomvalue, 'ispass': True})
        return regularobj

    # 特殊字符处理
    def string_special(self, special, lengthlist, randomvalue):
        '''
        special : 需要处理的特殊字符
        lengthlist : 测试长度的caselist
        randomvalue : 动态字符串
        '''
        input = special['input']
        specialobj = []
        if special['value'] == 'notinclude':
            if lengthlist:
                for length in lengthlist:
                    lengthispass = '长度合适' if length['ispass'] else '长度不合适'
                    value = exrex.getone('[^' + input[0] + ']{' + str(length['value']) + '}')
                    specialobj.append(
                        {'title': '不包含指定字符' + lengthispass, 'value': value + randomvalue,
                         'ispass': True and length['ispass']})
                    value = exrex.getone('[' + input[0] + ']{' + str(length['value']) + '}')
                    specialobj.append({'title': '包含指定字符' + lengthispass, 'value': value + randomvalue, 'ispass': False})
            else:
                for i in range(len(input[0])):
                    value = exrex.getone('[^' + input[0] + ']+')
                    specialobj.append({'title': '不包含指定字符', 'value': value + randomvalue, 'ispass': True})
                    value = exrex.getone('[' + input[0] + ']+')
                    specialobj.append({'title': '包含指定字符', 'value': value + randomvalue, 'ispass': False})
        elif special['value'] == 'include':
            if lengthlist:
                for length in lengthlist:
                    lengthispass = '长度合适' if length['ispass'] else '长度不合适'
                    if length['value'] - len(input[0]) > 0:
                        value = exrex.getone('[a-z][a-zA-Z0-9]{' + str(length['value'] - len(input[0])) + '}') + \
                                input[0]
                        specialobj.append(
                            {'title': '值包含指定字符' + lengthispass, 'value': value + randomvalue,
                             'ispass': True and length['ispass']})
                        value = exrex.getone('[^' + input[0] + ']{' + str(length['value'] - len(input[0])) + '}')
                        specialobj.append(
                            {'title': '不包含指定字符' + lengthispass, 'value': value + randomvalue, 'ispass': False})
            else:
                value = exrex.getone('[a-z][a-zA-Z0-9]+') + input[0]
                specialobj.append({'title': '包含指定字符', 'value': value + randomvalue, 'ispass': True})
                value = exrex.getone('[^' + input[0] + ']+')
                specialobj.append({'title': '不包含指定字符', 'value': value + randomvalue, 'ispass': False})

        return specialobj

    # 没有指定字符取值范围的统一处理
    def string_all(self,lengthlist,randomvalue):
        '''
        lengthlist : 取值长度的case列表
        randomvalue : 是否包含动态值,包含的话就是占位符,不包含则为空串
        '''
        allobj = []
        if lengthlist:
            for length in lengthlist:
                lengthispass = '长度合适' if length['ispass'] else '长度不合适'
                value = exrex.getone(self.regular['all'] + '{' + str(length['value']) + '}')
                allobj.append(
                    {'title': '合规字符串' + lengthispass, 'value': value + randomvalue,
                     'ispass': True and length['ispass']})
        else:
            for i in range(5):  #随机生成5条正向记录
                value = exrex.getone( self.regular['all'] + '+')
                allobj.append({'title': '符合要求的字符串', 'value': value + randomvalue, 'ispass': True})
        return allobj

    # 删除之前生成的case
    def del_case(self,caselist):
        for case in caselist:
            case.status = 0
            case.save()

    # 测试请求接口时,只挑选出一个可行组合
    def get_true(self,paramslist):
        params = {}
        for key,value in paramslist.items():
            params[key] = [x for x in value if x['ispass']]
        return params

    # 获取一个通用的结果为pass的数据
    def get_one(self,paramslist):
        params = {}
        if paramslist:
            for key,value in paramslist.items():
                if value:
                    params[key] = value[random.randint(0,len(value)-1)]
                else:
                    params[key] = value
        return params

    # 测试所有接口可选值进行组合
    def get_all(self,paramslist,paramtrue):
        params = []
        for key,value in paramslist.items():
            for v in value:
                param = self.get_one(paramtrue)
                param[key] = v
                params.append(param)
        return params

    # 往数据库插入新增的case
    def insert_case(self,apiobj,params,bodys,paramtrue,bodytrue):
        # 初始化case的固定值
        case = {
            'api':apiobj,
            'path':apiobj.path,
            'request_method':apiobj.request_method,
            'head':apiobj.base_head,
            'cookies':apiobj.cookies,
            'status':2,
            'body':{},
            'params':{},
        }
        caseids = []        # 存新增的case的ID
        for paramorbody in ['params','body']:
            list = params if paramorbody=='params' else bodys
            # 判断是否有可选的params或者body
            if list and list[0]:
                otherture = bodytrue if paramorbody == 'params' else paramtrue
                # 拼接请求体
                for l in list :
                    # 需要根据测试情况拼接的参数
                    case['case_name']=''
                    case['is_pass'] = True  # 最终的预期请求结果初始化
                    case['memo'] = '测试'+paramorbody+'参数\n'      # 详细的测试说明初始化
                    case[paramorbody] = {}  # 请求体初始化
                    # 循环请求参数
                    for key, value in l.items():
                        # 拼接用例名称,最终请求结果,详细说明
                        case['case_name'] += '【' + key + '】' + (value['title'] if not value['ispass'] else '')
                        case['is_pass'] = case['is_pass'] and value['ispass']
                        case['memo'] += '【' + key + '】\t' + value['title'] + '\t' + (
                            '合规字段\n' if value['ispass'] else '非法字段' + '\n')
                        # 拼接请求参数
                        case[paramorbody][key] = value['value']
                    # 获取另外一个参数的通用测试结果pass的数据
                    theotherpara = self.get_one(otherture)
                    for key, value in theotherpara.items():
                        theotherpara[key]=value['value']    # 字典结构简化
                    otherkey = 'body' if paramorbody=='params' else 'params'    #获取另一个参数名称
                    # 两个参数均转化为字符串存储
                    case[paramorbody] = json.dumps(case[paramorbody],ensure_ascii=False)
                    case[otherkey] = json.dumps(theotherpara,ensure_ascii=False)
                    case['case_name'] += '预期通过' if case['is_pass'] else '预期不通过'
                    case['expect'] = apiobj.expect_pass if case['is_pass'] else apiobj.expect_fail
                    # 保存apicase
                    apicase = ApiCase.objects.create(**case)
                    # 添加新增好的case Id,用于最后返回
                    caseids.append(apicase.id)
        return caseids

