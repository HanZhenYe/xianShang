import os
import html
import time
import random
from tool import aa
from tool import token
from django.core import mail
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from user.models import ImgYan, ImgList, EmailYan, User


# 生成图片验证
def create_yan(request):
    if request.method == 'GET':
        n = request.GET.get('n')
        if not n:
            return HttpResponse('n不能为空')
        if n == '1':
            for i in range(1, 31):
                img_tuple = aa.create_img()
                ImgYan.objects.create(id=i, code=img_tuple[0].lower(), path=img_tuple[1])

                img_all = ImgYan.objects.all()
                img_list = []
                for i in img_all:
                    img_list.append(i.id)
                data_imglist = ImgList.objects.filter(id=1)
                if not data_imglist:
                    ImgList.objects.create(id=1, img_list=str(img_list))
                else:
                    data_imglist[0].img_list = str(img_list)
        elif n == '0':
            img_all = ImgYan.objects.all()
            img_all.delete()
        else:
            return HttpResponse('n不正确')

        return HttpResponse('成功！')


# 获取图片验证
def get_yan(request):
    if request.method == 'GET':
        qq = request.GET.get('qq')
        if not qq:
            dic = {
                'code': 10100,
                'error': 'QQ号不能为空'
            }
            return JsonResponse(dic)
        try:
            qq = int(qq)
        except Exception as e:
            dic = {
                'code': 10101,
                'error': 'QQ格式不正确'
            }
            return JsonResponse(dic)

        img_sui = random.randint(1, 30)
        img_yan = ImgYan.objects.filter(id=img_sui)
        email = EmailYan.objects.filter(qq=qq)
        if not email:
            EmailYan.objects.create(qq=qq, img_code=img_yan[0].code)
        else:
            email[0].img_code = img_yan[0].code
            email[0].huo_shu += 1
            email[0].save()
        dic = {
            'code': 200,
            'img_path': img_yan[0].path
        }
        return JsonResponse(dic)


# 校验图片验证码正确性
def yan_img(request):
    if request.method == 'POST':
        qq = request.POST.get('qq')
        code = request.POST.get('code')
        if not qq:
            dic = {
                'code': 10100,
                'error': 'QQ号不能为空'
            }
            return JsonResponse(dic)
        if not code:
            dic = {
                'code': 10102,
                'error': '验证码错误'
            }
            return JsonResponse(dic)
        try:
            qq = int(qq)
        except Exception as e:
            dic = {
                'code': 10101,
                'error': 'QQ格式不正确'
            }
            return JsonResponse(dic)
        email = EmailYan.objects.filter(qq=qq)
        if not email:
            dic = {
                'code': 10103,
                'error': '请先获取图片验证码'
            }
            return JsonResponse(dic)
        code = code.lower()
        if email[0].img_code not in code:
            dic = {
                'code': 10102,
                'error': '验证码错误'
            }
            return JsonResponse(dic)
        dic = {
            'code': 200,
            'data': '安全认证通过，验证码以发送至您的QQ邮箱'
        }
        try:
            email_code = qq_yan(qq)
        except Exception as e:
            dic = {
                'code': 10110,
                'error': '当前QQ号不存在'
            }
            return JsonResponse(dic)
        email[0].email_code = email_code
        email[0].save()
        return JsonResponse(dic)


# 发送验证码至QQ邮箱
def qq_yan(qq):
    sui = random.randint(100000, 999999)
    mail.send_mail(
        subject='验证码',
        message=str(sui),
        from_email='1964998620@qq.com',
        recipient_list=['%s@qq.com' % qq],
    )
    return sui


# 登陆校验
def login(request):
    if request.method == 'POST':
        qq = request.POST.get('qq')
        code = request.POST.get('code')
        zt = request.POST.get('zt')
        if not qq:
            dic = {
                'code': 10102,
                'error': 'QQ号不能为空'
            }
            return JsonResponse(dic)
        if not code:
            dic = {
                'code': 10104,
                'error': '邮箱验证码不能为空'
            }
            return JsonResponse(dic)
        try:
            qq = int(qq)
        except Exception as e:
            dic = {
                'code': 10105,
                'error': 'QQ号格式不正确'
            }
            return JsonResponse(dic)
        try:
            code = int(code)
        except Exception as e:
            dic = {
                'code': 10108,
                'error': '验证码错误'
            }
            return JsonResponse(dic)
        email = EmailYan.objects.filter(qq=qq)
        if not email:
            dic = {
                'code': 10106,
                'error': 'QQ号不正确，请先使用该QQ号通过安全验证'
            }
            return JsonResponse(dic)
        if email[0].email_code != code:
            dic = {
                'code': 10107,
                'error': '验证码不正确'
            }
            return JsonResponse(dic)
        if zt == '0':
            tokens = token.token_encode(qq, 60 * 60 * 24)
        elif zt == '1':
            tokens = token.token_encode(qq, 60 * 60 * 24 * 15)
        else:
            dic = {
                'code': 10109,
                'error': '登陆异常'
            }
            return JsonResponse(dic)
        user = User.objects.filter(qq=qq)
        if not user:
            User.objects.create(qq=qq, name=qq, token=tokens.decode())
        user[0].token = tokens.decode()
        user[0].save()
        dic = {
            'code': 200,
            'data': tokens.decode()
        }
        email[0].delete()
        return JsonResponse(dic)


# 个人中心
@token.logging_check('GET')
def geren(request):
    if request.method == 'GET':
        user = request.user
        # 获得当前年份
        date1 = time.localtime(time.time()).tm_year
        # 获取用户生日年份
        date2 = user.birth_date.year

        user_date = {
            'qq': user.qq,
            'name': user.name,
            'age': user.age,
            'nian': date1 - date2,
            'birth_date': user.birth_date,
            'portrait': str(user.portrait),
            'my_occ': user.my_occ,
            'my_cour_series': user.my_cour_series,
            'my_cour': user.my_cour,
            'my_res': user.my_res,
            'my_not': user.my_not,
            'coll_occ': user.coll_occ,
            'coll_cour_series': user.coll_cour_series,
            'coll_cour': user.coll_cour,
            'coll_res': user.coll_res,
            'coll_not': user.coll_not
        }
        dic = {
            'code': 200,
            'data': user_date
        }

        return JsonResponse(dic)


# 用户信息修改
@token.logging_check('POST')
def modify(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ages = request.POST.get('age')
        birth_date = request.POST.get('shen')
        portrait = request.FILES.get('myFile')

        user = request.user
        # 用户输入转义
        name = html.escape(name)
        if ages == '0':
            age = '女'
        else:
            age = '男'

        user.name = name
        user.age = age
        user.birth_date = birth_date
        if portrait:
            try:
                aa.delete_file(os.path.join('media/', str(user.portrait)))
            except Exception as e:
                print('用户头像删除失败')
                print(e)
            user.portrait = portrait
        user.save()
        return JsonResponse({'code': 200})

