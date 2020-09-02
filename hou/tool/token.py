import jwt
import time
from user.models import User, Examine
from django.http import JsonResponse

KOKEN_KEY = '@$?><254QW'
qian_server = 'http://106.53.8.216/user/login'
#qian_server = 'http://127.0.0.1:5000/user/login'


# 生成token
def token_encode(qq, times):
    payload = {
        'exp': time.time() + times,
        'qq': qq
    }
    token = jwt.encode(payload, KOKEN_KEY, 'HS256')
    return token


# token解密
def token_decode(token):
    return jwt.decode(token, KOKEN_KEY, 'HS256')


# 三层装饰器
def logging_check(*method):
    def _logging_check(func):
        def warapps(request, *args, **kwargs):
            # method中没有值
            if not method:
                return func(request, *args, **kwargs)
            else:
                # 判断是否需要校验
                if request.method not in method:
                    return func(request, *args, **kwargs)
                else:
                    # 该处要进行token的校验
                    # 从请求头中取出token
                    token = request.META.get('HTTP_AUTHORIZATION')
                    # token为空则表示未登陆
                    if not token:
                        dic = {
                            'code': 10106,
                            'data': qian_server
                        }
                        return JsonResponse(dic)
                    else:
                        # 异常则表示, token过期或非我方签发的token
                        try:
                            res = token_decode(token)
                        except Exception as e:
                            dic = {
                                'code': 10106,
                                'data': qian_server
                            }
                            return JsonResponse(dic)
                        qq = res.get('qq')
                        if not qq:
                            dic = {
                                'code': 10106,
                                'data': qian_server
                            }
                            return JsonResponse(dic)
                        try:
                            qq = int(qq)
                        except Exception as e:
                            dic = {
                                'code': 10106,
                                'data': qian_server
                            }
                            return JsonResponse(dic)
                        user = User.objects.filter(qq=qq)
                        if not user:
                            dic = {
                                'code': 10106,
                                'data': qian_server
                            }
                            return JsonResponse(dic)
                        request.user = user[0]
            return func(request, *args, **kwargs)
        return warapps
    return _logging_check


# 校验用户状态
def user_check(*method):
    def _logging_check(func):
        def warapps(request, *args, **kwargs):
            # method中没有值
            if not method:
                return func(request, *args, **kwargs)
            else:
                # 判断是否需要校验
                if request.method not in method:
                    return func(request, *args, **kwargs)
                else:
                    # 该处要进行token的校验
                    # 从请求头中取出token
                    token = request.META.get('HTTP_AUTHORIZATION')
                    # token为空则表示未登陆
                    if token == 'null':
                        # 0表示没有登陆
                        request.user_type = 0
                        return func(request, *args, **kwargs)
                    else:
                        # 异常则表示, token过期或非我方签发的token
                        try:
                            res = token_decode(token)
                        except Exception as e:
                            request.user_type = 0
                            return func(request, *args, **kwargs)

                        qq = res.get('qq')
                        qq = int(qq)
                        user = User.objects.filter(qq=qq)
                        request.user_type = -1
                        exadmine = Examine.objects.filter(qq=qq)
                        # 判断是否是管理员
                        if exadmine:
                            request.user_type = 1
                        request.user = user[0]
            return func(request, *args, **kwargs)
        return warapps
    return _logging_check
