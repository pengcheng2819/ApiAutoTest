# 作者      : pengcheng
# 创建时间  : 2020/12/1 16:27 
from functools import wraps
from rest_framework.response import Response
from rest_framework import status

# 请求返回值跟错误捕捉装饰器
def try_result(msg=''):
    def try_decorator(func):
        @wraps(func)
        def wrapTheFunction(*args, **kwargs):
            try:
                data = func(*args, **kwargs)
                result = {
                    'msg': msg+"成功！",
                    'status': 1
                }
                if data:
                    result['data'] = data
                if isinstance(data,Response):   #当data为response类型时,直接返回
                    return data
                else:
                    return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                result = {
                    'msg': msg+"失败！失败信息为:" + str(e),
                    'status': 0
                }
                return Response(result)
        return wrapTheFunction
    return try_decorator

# @try_result('yrert')
# def aa(a,b):
#     print(a+b)





# 用户授权装饰器
# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             authenticate()
#         return f(*args, **kwargs)
#
#     return decorated


# if __name__ == '__main__':
#     aa(10,20)
#     print(aa.__name__)