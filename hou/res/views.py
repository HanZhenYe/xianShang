import os
import json
import html
from tool import aa
from .models import *
from tool import token
from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse, QueryDict


# 用户资源
@token.logging_check('GET', 'POST')
def user_res(request):
    # 获取用户资源
    if request.method == 'GET':
        user = request.user
        user_occ = user.occ_set.all()
        user_cour_series = user.courseries_set.all()
        user_cour = user.cour_set.all()
        user_res = user.res_set.all()
        occ_list = []
        for i in user_occ:
            dic = {
                'id': i.id,
                'title': i.title,
                'synopsys': i.synopsys
            }
            occ_list.append(dic)

        cour_series_list = []
        for i in user_cour_series:
            dic = {
                'id': i.id,
                'title': i.title,
                'synopsys': i.synopsys
            }
            cour_series_list.append(dic)

        cour_list = []
        for i in user_cour:
            dic = {
                'id': i.id,
                'title': i.title,
                'synopsys': i.synopsys
            }
            cour_list.append(dic)

        res_list = []
        for i in user_res:
            dic = {
                'id': i.id,
                'title': i.title,
                'synopsys': i.synopsys
            }
            res_list.append(dic)

        colls = user.collection_set.all()

        coll_occ = []
        for res in colls.filter(res_type='occ'):
            re = Occ.objects.filter(id=res.type_id)
            if not re:
                res.delete()
                continue
            dic = {
                'id': re[0].id,
                'title': re[0].title,
                'synopsys': re[0].synopsys
            }
            coll_occ.append(dic)

        coll_course = []
        for res in colls.filter(res_type='cos'):
            re = CourSeries.objects.filter(id=res.type_id)
            if not re:
                res.delete()
                continue
            dic = {
                'id': re[0].id,
                'title': re[0].title,
                'synopsys': re[0].synopsys
            }
            coll_course.append(dic)

        coll_cour = []
        for res in colls.filter(res_type='cou'):
            re = Cour.objects.filter(id=res.type_id)
            if not re:
                res.delete()
                continue
            dic = {
                'id': re[0].id,
                'title': re[0].title,
                'synopsys': re[0].synopsys
            }
            coll_cour.append(dic)

        coll_res = []
        for res in colls.filter(res_type='res'):
            re = Res.objects.filter(id=res.type_id)
            if not re:
                res.delete()
                continue
            dic = {
                'id': re[0].id,
                'title': re[0].title,
                'synopsys': re[0].synopsys
            }
            coll_res.append(dic)

        dic = {
            'code': 200,
            'data': {
                'occ': occ_list,
                'cour_series': cour_series_list,
                'cour': cour_list,
                'res': res_list,
                'coll_occ': coll_occ,
                'coll_course': coll_course,
                'coll_cour': coll_cour,
                'coll_res': coll_res
            }
        }
        return JsonResponse(dic)

    # 用户创建资源
    if request.method == 'POST':
        user = request.user
        res_typr = request.POST.get('res_type')
        name = request.POST.get('name')
        synopsys = request.POST.get('synopsys')
        cover = request.FILES.get('myFile')
        if not res_typr:
            dic = {
                'code': 10204,
                'error': '资源类型不能为空'
            }
            return JsonResponse(dic)
        if not name:
            dic = {
                'code': 10205,
                'error': '标题不能为空'
            }
            return JsonResponse(dic)
        if not synopsys:
            dic = {
                'code': 10206,
                'error': '简介不能为空'
            }
            return JsonResponse(dic)
        if not cover:
            dic = {
                'code': 10207,
                'error': '封面不能为空'
            }
            return JsonResponse(dic)

        # 用户输入转义
        name = html.escape(name)
        synopsys = html.escape(synopsys)

        try:
            # 创建职业
            if res_typr == 'occ':
                Occ.objects.create(title=name, synopsys=synopsys, cover=cover, user=user, route='[]')
                user.my_occ += 1

            # 创建课程系列
            elif res_typr == 'cour_series':
                CourSeries.objects.create(title=name, synopsys=synopsys, cover=cover,
                                          user=user, course_list='')
                user.my_cour_series += 1

            # 创建课程
            elif res_typr == 'cour':
                Cour.objects.create(title=name, synopsys=synopsys, cover=cover, user=user, directory='[]')
                user.my_cour += 1

            # 创建资源
            elif res_typr == 'res':
                Res.objects.create(title=name, synopsys=synopsys, cover=cover, user=user)
                user.my_res += 1

            else:
                dic = {
                    'code': 10203,
                    'error': '创建失败，资源类型不正确'
                }
                return JsonResponse(dic)
            user.save()

        except Exception as e:
            print(e)
            dic = {
                'code': 20108,
                'error': '创建失败'
            }
            return JsonResponse(dic)

        return JsonResponse({'code': 200, 'data': '创建成功'})


# 资源管理
@token.logging_check('GET', 'DELETE')
def res_admin(request):
    if request.method == 'GET':
        user = request.user
        res_id = request.GET.get('res_id')
        res_type = request.GET.get('res_type')
        if not res_type:
            dic = {
                'code': 10210,
                'error': '数据类型不能为空'
            }
            return JsonResponse(dic)

        if not res_id:
            dic = {
                'code': 10211,
                'error': '资源ID不能为可空'
            }
            return JsonResponse(dic)

        try:
            res_id = int(res_id)
        except Exception as e:
            dic = {
                'code': 10212,
                'error': '资源ID不合格'
            }
            return JsonResponse(dic)

        # 获取职业信息
        if res_type == 'occ':
            occs = Occ.objects.filter(id=res_id, user=user)
            if not occs:
                dic = {
                    'code': 10213,
                    'error': '当前职业不存在'
                }
                return JsonResponse(dic)
            occ = occs[0]

            routes = occ.route
            routes = json.loads(routes)
            routes_list = []
            for jie in routes:
                cour_list = []
                for cour_id in jie[1].split(','):
                    if cour_id == '':
                        continue
                    cours = Cour.objects.filter(id=cour_id, user=user)
                    if not cours:
                        continue
                    cour = cours[0]
                    cour_dic = {
                        'id': cour.id,
                        'title': cour.title,
                        'cover': str(cour.cover)
                    }
                    cour_list.append(cour_dic)
                routes_list.append({
                    'jie': jie[0],
                    'cour_list': cour_list
                })

            occ_data = {
                'title': occ.title,
                'synopsys': occ.synopsys,
                'cover': str(occ.cover),
                'overt': occ.overt,
                'audit': occ.audit,
                'routes': routes_list
            }
            dic = {
                'code': 200,
                'data': occ_data
            }
            return JsonResponse(dic)

        # 获取课程系列信息
        elif res_type == 'cour_series':
            coursers = CourSeries.objects.filter(id=res_id, user=user)
            if not coursers:
                dic = {
                    'code': 10213,
                    'error': '当前系列不存在'
                }
                return JsonResponse(dic)
            courser = coursers[0]

            cour_str = courser.course_list
            cour_id_list = cour_str.split(',')
            cour_list = []
            for cour_id in cour_id_list:
                if not cour_id:
                    continue
                cours = Cour.objects.filter(id=cour_id, user=user)
                if not cours:
                    continue
                cour = cours[0]
                cour_dic = {
                    'id': cour.id,
                    'title': cour.title,
                    'cover': str(cour.cover)
                }
                cour_list.append(cour_dic)

            courser_data = {
                'title': courser.title,
                'synopsys': courser.synopsys,
                'cover': str(courser.cover),
                'overt': courser.overt,
                'audit': courser.audit,
                'cour_list': cour_list
            }
            dic = {
                'code': 200,
                'data': courser_data
            }
            return JsonResponse(dic)

        # 获取课程信息
        elif res_type == 'cour':
            cours = Cour.objects.filter(id=res_id, user=user)
            if not cours:
                dic = {
                    'code': 10213,
                    'error': '当前系列不存在'
                }
                return JsonResponse(dic)
            cour = cours[0]
            dirs = cour.directory
            dir = json.loads(dirs)
            courser_data = {
                'title': cour.title,
                'synopsys': cour.synopsys,
                'cover': str(cour.cover),
                'overt': cour.overt,
                'audit': cour.audit,
                'dir': dir
            }
            dic = {
                'code': 200,
                'data': courser_data
            }
            return JsonResponse(dic)

        # 获取资源信息
        elif res_type == 'res':
            ress = Res.objects.filter(id=res_id, user=user)
            if not ress:
                dic = {
                    'code': 10213,
                    'error': '当前资源链接不存在'
                }
                return JsonResponse(dic)
            res = ress[0]

            res_data = {
                'title': res.title,
                'synopsys': res.synopsys,
                'cover': str(res.cover),
                'overt': res.overt,
                'audit': res.audit,
                'link': res.limk
            }
            dic = {
                'code': 200,
                'data': res_data
            }
            return JsonResponse(dic)

        # 获取笔记信息
        elif res_type == 'note':
            pass
        else:
            dic = {
                'code': 10219,
                'error': '资源类型异常'
            }
            return JsonResponse(dic)

    elif request.method == 'DELETE':
        user = request.user
        DELETE = QueryDict(request.body)
        res_type = DELETE.get('res_type')
        res_id = DELETE.get('res_id')
        if not res_type:
            dic = {
                'code': 10221,
                'error': '资源类型不能为空'
            }
            return JsonResponse(dic)
        if not res_id:
            dic = {
                'code': 10222,
                'error': '资源ID不能为空'
            }
            return JsonResponse(dic)
        try:
            res_id = int(res_id)
        except Exception as e:
            dic = {
                'code': 10223,
                'error': '资源类型不正确'
            }
            return JsonResponse(dic)

        if res_type == 'occ':
            occs = Occ.objects.filter(id=res_id, user=user)
            if not occs:
                dic = {
                    'code': 10225,
                    'error': '删除失败, 您没有该职业'
                }
                return JsonResponse(dic)
            try:
                aa.delete_file(os.path.join('media/', str(occs[0].cover)))
            except Exception as e:
                print('职业封面修改失败')
                print(e)
            occs[0].delete()
            user.my_occ -= 1

        elif res_type == 'cour_series':
            courser = CourSeries.objects.filter(id=res_id, user=user)
            if not courser:
                dic = {
                    'code': 10225,
                    'error': '删除失败, 您没有该系列'
                }
                return JsonResponse(dic)
            try:
                aa.delete_file(os.path.join('media/', str(courser[0].cover)))
            except Exception as e:
                print('系列封面修改失败')
                print(e)
            courser[0].delete()
            user.my_cour_series -= 1

        elif res_type == 'cour':
            cours = Cour.objects.filter(id=res_id, user=user)
            if not cours:
                dic = {
                    'code': 10225,
                    'error': '删除失败, 您没有该系列'
                }
                return JsonResponse(dic)
            try:
                aa.delete_file(os.path.join('media/', str(cours[0].cover)))
            except Exception as e:
                print('课程封面修改失败')
                print(e)
            cours[0].delete()
            user.my_cour -= 1

        elif res_type == 'res':
            res = Res.objects.filter(id=res_id, user=user)
            if not res:
                dic = {
                    'code': 10225,
                    'error': '删除失败, 您没有该资源'
                }
                return JsonResponse(dic)
            try:
                aa.delete_file(os.path.join('media/', str(res[0].cover)))
            except Exception as e:
                print('资源链接封面修改失败')
                print(e)
            res[0].delete()
            user.my_res -= 1

        else:
            dic = {
                'code': 10224,
                'error': '资源类型不正确'
            }
            return JsonResponse(dic)

        user.save()
        dic = {
            'code': 200
        }
        return JsonResponse(dic)


# 获取课程列表
@token.logging_check('GET')
def get_cour(request):
    if request.method == 'GET':
        user = request.user
        cours = user.cour_set.all()
        cour_list = []
        for cour in cours:
            cour_dic = {
                'id': cour.id,
                'title': cour.title,
                'cover': str(cour.cover)
            }
            cour_list.append(cour_dic)
        dic = {
            'code': 200,
            'data': cour_list
        }
        return JsonResponse(dic)


# 资源修改
@token.logging_check('POST')
def res_update(request):
    if request.method == 'POST':
        user = request.user
        res_id = request.POST.get('res_id')
        res_type = request.POST.get('res_type')
        title = request.POST.get('title')
        synopsys = request.POST.get('synopsys')
        cover = request.FILES.get('myFile')
        overt = request.POST.get('overt')

        if not res_type:
            dic = {
                'code': 10214,
                'error': '资源类型不能为空'
            }
            return JsonResponse(dic)
        if not title:
            dic = {
                'code': 10215,
                'error': '标题不能为空'
            }
            return JsonResponse(dic)
        if not synopsys:
            dic = {
                'code': 10216,
                'error': '简介不能为空'
            }
            return JsonResponse(dic)
        if not overt:
            dic = {
                'code': 10217,
                'error': '公开状态不能为空'
            }
            return JsonResponse(dic)
        try:
            res_id = int(res_id)
        except Exception as e:
            dic = {
                'code': 10220,
                'error': '资源ID不正确'
            }
            return JsonResponse(dic)

        if res_type == 'occ':
            route = request.POST.get('route', '[]')
            occs = Occ.objects.filter(id=res_id, user=user)
            if not occs:
                dic = {
                    'code': 10221,
                    'error': '对不起，您没有该职业修改权限'
                }
                return JsonResponse(dic)
            occ = occs[0]
            occ.title = title
            occ.synopsys = synopsys
            if cover:
                try:
                    aa.delete_file(os.path.join('media/', str(occ.cover)))
                    occ.cover = cover
                except Exception as e:
                    print('职业封面修改失败')
                    print(e)
            if overt == 'true':
                occ.overt = True
            else:
                occ.overt = False
            occ.route = route
            occ.audit = '未'
            occ.save()
            er = ExamineRes.objects.filter(type_id=res_id, res_type='occ')
            if er:
                er.delete()
            dic = {
                'code': 200,
                'data': '修改完成'
            }
            return JsonResponse(dic)

        elif res_type == 'cour_series':
            course_list = request.POST.get('course_list', ' ')
            cour_series = CourSeries.objects.filter(id=res_id, user=user)
            if not cour_series:
                dic = {
                    'code': 10221,
                    'error': '对不起，您没有该系列修改权限'
                }
                return JsonResponse(dic)
            cour_ser = cour_series[0]
            cour_ser.title = title
            cour_ser.synopsys = synopsys
            if cover:
                try:
                    aa.delete_file(os.path.join('media/', str(cour_ser.cover)))
                    cour_ser.cover = cover
                except Exception as e:
                    print('系列封面修改失败')
                    print(e)
            if overt == 'true':
                cour_ser.overt = True
            else:
                cour_ser.overt = False
            cour_ser.course_list = course_list
            cour_ser.audit = '未'
            cour_ser.save()
            er = ExamineRes.objects.filter(type_id=res_id, res_type='cos')
            if er:
                er.delete()
            dic = {
                'code': 200,
                'data': '修改完成'
            }
            return JsonResponse(dic)

        elif res_type == 'cour':
            directory = request.POST.get('dir', '[]')
            cours = Cour.objects.filter(id=res_id, user=user)
            if not cours:
                dic = {
                    'code': 10221,
                    'error': '对不起，您没有该课程修改权限'
                }
                return JsonResponse(dic)
            cour = cours[0]
            cour.title = title
            cour.synopsys = synopsys
            if cover:
                try:
                    aa.delete_file(os.path.join('media/', str(cour.cover)))
                    cour.cover = cover
                except Exception as e:
                    print('课程封面修改失败')
                    print(e)
            if overt == 'true':
                cour.overt = True
            else:
                cour.overt = False
            cour.directory = directory
            cour.audit = '未'
            cour.save()
            er = ExamineRes.objects.filter(type_id=res_id, res_type='cou')
            if er:
                er.delete()
            dic = {
                'code': 200,
                'data': '修改完成'
            }
            return JsonResponse(dic)

        elif res_type == 'res':
            ress = Res.objects.filter(id=res_id, user=user)
            if not ress:
                dic = {
                    'code': 10221,
                    'error': '对不起，您没有该资源链接的修改权限'
                }
                return JsonResponse(dic)
            link = request.POST.get('link')
            if not link:
                dic = {
                    'code': 10230,
                    'error': '资源链接不能为空'
                }
                return JsonResponse(dic)
            res = ress[0]
            res.title = title
            res.synopsys = synopsys
            res.limk = link
            if cover:
                try:
                    aa.delete_file(os.path.join('media/', str(res.cover)))
                    res.cover = cover
                except Exception as e:
                    print('课程封面修改失败')
                    print(e)
            if overt == 'true':
                res.overt = True
            else:
                res.overt = False
            res.audit = '未'
            res.save()
            er = ExamineRes.objects.filter(type_id=res_id, res_type='res')
            if er:
                er.delete()
            dic = {
                'code': 200,
                'data': '修改完成'
            }
            return JsonResponse(dic)

        elif res_type == 'note':
            pass
        else:
            dic = {
                'code': 10218,
                'error': '资源类型错误'
            }
            return JsonResponse(dic)


# 显示资源
@token.user_check('GET')
def get_res(request):
    if request.method == 'GET':
        user_type = request.user_type
        res_tyoe = request.GET.get('res_type')
        res_id = request.GET.get('res_id')
        shou = 0

        if request.method == 'GET':
            if request.user_type == 0:
                if_login = False
            else:
                if_login = True

        if not res_tyoe:
            return JsonResponse({'code': 10227})

        if not res_id:
            return JsonResponse({'code': 10227})
        try:
            res_id = int(res_id)
        except Exception as e:
            return JsonResponse({'code': 10227})

        # 显示职业信息
        if res_tyoe == 'occ':
            occs = Occ.objects.filter(id=res_id)
            if not occs:
                return JsonResponse({'code': 10227})

            occ = occs[0]
            # 游客身份
            if not user_type:
                if not occ.overt:
                    return JsonResponse({'code': 10227})
                elif occ.audit not in '通':
                    return JsonResponse({'code': 10227})
            else:
                user = request.user
                shous = user.collection_set.filter(res_type='occ', type_id=res_id)
                if shous:
                    shou = 1

                # 排除非作者
                if user and (user_type != 1):
                    if user.qq != occ.user.qq:
                        if not occ.overt:
                            return JsonResponse({'code': 10227})
                        elif occ.audit not in '通':
                            return JsonResponse({'code': 10227})

            # 职业路线转化
            routes = occ.route
            routes = json.loads(routes)
            routes_list = []
            for jie in routes:
                cour_list = []
                for cour_id in jie[1].split(','):
                    if cour_id == '':
                        continue
                    cours = Cour.objects.filter(id=cour_id)
                    if not cours:
                        continue
                    cour = cours[0]
                    cour_dic = {
                        'id': cour.id,
                        'title': cour.title,
                        'cover': str(cour.cover),
                        'collection': cour.collection,
                    }
                    cour_list.append(cour_dic)
                routes_list.append({
                    'jie': jie[0],
                    'cour_list': cour_list,
                })

            occ_dic = {
                'name': occ.user.name,
                'title': occ.title,
                'synopsys': occ.synopsys,
                'collection': occ.collection,
                'route': routes_list,
                'shou': shou,
                'if_login': if_login
            }
            dic = {
                'code': 200,
                'data': occ_dic
            }
            return JsonResponse(dic)

        # 显示课程系列
        elif res_tyoe == 'cour_series':
            coursers = CourSeries.objects.filter(id=res_id)
            if not coursers:
                return JsonResponse({'code': 10227})

            courser = coursers[0]
            # 游客身份
            if not user_type:
                if not courser.overt:
                    return JsonResponse({'code': 10227})
                elif courser.audit not in '通':
                    return JsonResponse({'code': 10227})
            else:
                user = request.user
                shous = user.collection_set.filter(res_type='cos', type_id=res_id)
                if shous:
                    shou = 1

                # 排除非作者
                if user and (user_type != 1):
                    if user.qq != courser.user.qq:
                        if not courser.overt:
                            return JsonResponse({'code': 10227})
                        elif courser.audit not in '通':
                            return JsonResponse({'code': 10227})

            cour_str = courser.course_list
            cour_id_list = cour_str.split(',')
            cour_list = []
            for cour_id in cour_id_list:
                if not cour_id:
                    continue
                cours = Cour.objects.filter(id=cour_id)
                if not cours:
                    continue
                cour = cours[0]
                cour_dic = {
                    'id': cour.id,
                    'title': cour.title,
                    'cover': str(cour.cover),
                    'collection': cour.collection,
                }
                cour_list.append(cour_dic)

            courser_data = {
                'name': courser.user.name,
                'title': courser.title,
                'synopsys': courser.synopsys,
                'collection': courser.collection,
                'cour_list': cour_list,
                'shou': shou,
                'if_login': if_login
            }
            dic = {
                'code': 200,
                'data': courser_data
            }
            return JsonResponse(dic)

        # 显示课程
        elif res_tyoe == 'cour':
            cours = Cour.objects.filter(id=res_id)
            if not cours:
                return JsonResponse({'code': 10227})
            cour = cours[0]
            # 游客身份
            if not user_type:
                if not cour.overt:
                    return JsonResponse({'code': 10227})
                elif cour.audit not in '通':
                    return JsonResponse({'code': 10227})
            else:
                user = request.user
                shous = user.collection_set.filter(res_type='cou', type_id=res_id)
                if shous:
                    shou = 1

                # 排除非作者
                if user and (user_type != 1):
                    if user.qq != cour.user.qq:
                        if not cour.overt:
                            return JsonResponse({'code': 10227})
                        elif cour.audit not in '通':
                            return JsonResponse({'code': 10227})

            dirs = cour.directory
            dir = json.loads(dirs)
            cour_dic = {
                'name': cour.user.name,
                'title': cour.title,
                'synopsys': cour.synopsys,
                'collection': cour.collection,
                'dir': dir,
                'shou': shou,
                'if_login': if_login
            }
            dic = {
                'code': 200,
                'data': cour_dic
            }
            return JsonResponse(dic)

        # 显示资源链接
        elif res_tyoe == 'res':
            ress = Res.objects.filter(id=res_id)
            if not ress:
                return JsonResponse({'code': 10227})

            res = ress[0]
            # 游客身份
            if not user_type:
                if not res.overt:
                    return JsonResponse({'code': 10227})
                elif res.audit not in '通':
                    return JsonResponse({'code': 10227})
            else:
                user = request.user
                shous = user.collection_set.filter(res_type='res', type_id=res_id)
                if shous:
                    shou = 1

                # 排除非作者
                if user and (user_type != 1):
                    if user.qq != res.user.qq:
                        if not res.overt:
                            return JsonResponse({'code': 10227})
                        elif res.audit not in '通':
                            return JsonResponse({'code': 10227})

            res_dic = {
                'name': res.user.name,
                'title': res.title,
                'synopsys': res.synopsys,
                'collection': res.collection,
                'link': res.limk,
                'shou': shou,
                'if_login': if_login
            }
            dic = {
                'code': 200,
                'data': res_dic
            }
            return JsonResponse(dic)

        else:
            dic = {
                'code': 10231,
                'error': '资源类型不正确'
            }
            return JsonResponse(dic)


# 主页
@token.user_check('GET')
def index(request):
    if request.method == 'GET':
        if request.user_type == 0:
            if_login = False
        else:
            if_login = True
        # 获取平台
        pla = Platfrom.objects.all()
        pla_list = []
        for p in pla:
            pla_dic = {
                'name': p.name,
                'cover': str(p.cover),
                'link': p.limk
            }
            pla_list.append(pla_dic)

        # 获取职业
        occs = Occ.objects.filter(overt=True, audit='通')
        occ = occs.order_by('-collection')[0:4]
        occ_list = []
        for o in occ:
            occ_dic = {
                'id': o.id,
                'name': o.user.name,
                'title': o.title,
                'cover': str(o.cover),
                'collection': o.collection
            }
            occ_list.append(occ_dic)

        # 获取系列
        coursers = CourSeries.objects.filter(overt=True, audit='通')
        courser = coursers.order_by('-collection')[0:4]
        courser_list = []
        for o in courser:
            courser_dic = {
                'id': o.id,
                'name': o.user.name,
                'title': o.title,
                'cover': str(o.cover),
                'collection': o.collection
            }
            courser_list.append(courser_dic)

        # 获取课程
        cours = Cour.objects.filter(overt=True, audit='通')
        cour = cours.order_by('-collection')[0:4]
        cour_list = []
        for o in cour:
            cour_dic = {
                'id': o.id,
                'name': o.user.name,
                'title': o.title,
                'cover': str(o.cover),
                'collection': o.collection
            }
            cour_list.append(cour_dic)

        # 获取资源
        ress = Res.objects.filter(overt=True, audit='通')
        res = ress.order_by('-collection')[0:4]
        res_list = []
        for o in res:
            res_dic = {
                'id': o.id,
                'name': o.user.name,
                'title': o.title,
                'cover': str(o.cover),
                'collection': o.collection
            }
            res_list.append(res_dic)

        data = {
            'pla': pla_list,
            'occ': occ_list,
            'courser': courser_list,
            'cour': cour_list,
            'res': res_list,
            'if_login': if_login
        }

        dic = {
            'code': 200,
            'data': data
        }
        return JsonResponse(dic)


# 收藏
@token.logging_check('POST')
def shou(request):
    if request.method == 'POST':
        user = request.user
        st = request.POST.get('st')
        res_id = request.POST.get('res_id')
        res_type = request.POST.get('res_type')
        if st not in ['k', 's']:
            dic = {
                'code': 10233,
                'error': '收藏类型不正常'
            }
            return JsonResponse(dic)
        if not res_id:
            dic = {
                'code': 10233,
                'error': '职业ID不能为空'
            }
            return JsonResponse(dic)
        try:
            res_id = int(res_id)
        except Exception as e:
            dic = {
                'code': 10233,
                'error': '职业ID错误'
            }
            return JsonResponse(dic)
        if not res_type:
            dic = {
                'code': 10233,
                'error': '资源类型不能为空'
            }
            return JsonResponse(dic)

        if res_type not in ['occ', 'cos', 'cou', 'res']:
            dic = {
                'code': 10233,
                'error': '资源类型不正确'
            }
            return JsonResponse(dic)

        colls = user.collection_set.filter(res_type=res_type, type_id=res_id)

        if st == 's':
            if not colls:
                Collection.objects.create(res_type=res_type, type_id=res_id, user=user)
        if st == 'k':
            if colls:
                colls[0].delete()
        if res_type == 'occ':
            occs = Occ.objects.filter(id=res_id)
            if not occs:
                dic = {
                    'code': 10233,
                    'error': '当前职业不存在'
                }
                return JsonResponse(dic)
            # 改变当前职业收藏数量
            if st == 's':
                try:
                    Occ.objects.filter(id=res_id).update(collection=F('collection')+1)
                    user.coll_occ += 1
                    user.save()
                except Exception as e:
                    dic = {
                        'code': 10233,
                        'error': '收藏失败,当前职业不存在'
                    }
                    return JsonResponse(dic)
            else:
                try:
                    Occ.objects.filter(id=res_id).update(collection=F('collection')-1)
                    user.coll_occ -= 1
                    user.save()
                except Exception as e:
                    dic = {
                        'code': 10233,
                        'error': '收藏失败,当前职业不存在'
                    }
                    return JsonResponse(dic)

        elif res_type == 'cos':
            courser = CourSeries.objects.filter(id=res_id)
            if not courser:
                dic = {
                    'code': 10233,
                    'error': '当前职业不存在'
                }
                return JsonResponse(dic)
            # 改变当前职业收藏数量
            if st == 's':
                try:
                    CourSeries.objects.filter(id=res_id).update(collection=F('collection')+1)
                    user.coll_cour_series += 1
                    user.save()
                except Exception as e:
                    dic = {
                        'code': 10233,
                        'error': '收藏失败,当前职业不存在'
                    }
                    return JsonResponse(dic)
            else:
                try:
                    CourSeries.objects.filter(id=res_id).update(collection=F('collection')-1)
                    user.coll_cour_series -= 1
                    user.save()
                except Exception as e:
                    dic = {
                        'code': 10233,
                        'error': '收藏失败,当前职业不存在'
                    }
                    return JsonResponse(dic)

        elif res_type == 'cou':
            cour = Cour.objects.filter(id=res_id)
            if not cour:
                dic = {
                    'code': 10233,
                    'error': '当前职业不存在'
                }
                return JsonResponse(dic)
            # 改变当前职业收藏数量
            if st == 's':
                try:
                    Cour.objects.filter(id=res_id).update(collection=F('collection') + 1)
                    user.coll_cour += 1
                    user.save()
                except Exception as e:
                    dic = {
                        'code': 10233,
                        'error': '收藏失败,当前职业不存在'
                    }
                    return JsonResponse(dic)
            else:
                try:
                    Cour.objects.filter(id=res_id).update(collection=F('collection') - 1)
                    user.coll_cour -= 1
                    user.save()
                except Exception as e:
                    dic = {
                        'code': 10233,
                        'error': '收藏失败,当前职业不存在'
                    }
                    return JsonResponse(dic)

        elif res_type == 'res':
            res = Res.objects.filter(id=res_id)
            if not res:
                dic = {
                    'code': 10233,
                    'error': '当前职业不存在'
                }
                return JsonResponse(dic)
            # 改变当前职业收藏数量
            if st == 's':
                try:
                    Res.objects.filter(id=res_id).update(collection=F('collection') + 1)
                    user.coll_res += 1
                    user.save()
                except Exception as e:
                    dic = {
                        'code': 10233,
                        'error': '收藏失败,当前职业不存在'
                    }
                    return JsonResponse(dic)
            else:
                try:
                    Res.objects.filter(id=res_id).update(collection=F('collection') - 1)
                    user.coll_res -= 1
                    user.save()
                except Exception as e:
                    dic = {
                        'code': 10233,
                        'error': '收藏失败,当前职业不存在'
                    }
                    return JsonResponse(dic)

        dic = {
            'code': 200,
        }
        return JsonResponse(dic)


# 获取审核
@token.user_check('GET')
def examine(request):
    if request.method == 'GET':
        if request.user_type != 1:
            return JsonResponse({'code': 10234})

        ex = ExamineRes.objects.all()
        occ_list = []
        for occ in ex.filter(res_type='occ'):
            dic = {
                'qq': occ.qq,
                'title': occ.title,
                'type_id': occ.type_id
            }
            occ_list.append(dic)

        course_list = []
        for cos in ex.filter(res_type='cos'):
            dic = {
                'qq': cos.qq,
                'title': cos.title,
                'type_id': cos.type_id
            }
            course_list.append(dic)

        cour_list = []
        for cou in ex.filter(res_type='cou'):
            dic = {
                'qq': cou.qq,
                'title': cou.title,
                'type_id': cou.type_id
            }
            cour_list.append(dic)

        res_list = []
        for res in ex.filter(res_type='res'):
            dic = {
                'qq': res.qq,
                'title': res.title,
                'type_id': res.type_id
            }
            res_list.append(dic)

        ex_dic = {
            'occ': occ_list,
            'cos': course_list,
            'cou': cour_list,
            'res': res_list
        }
        dic = {
            'code': 200,
            'data': ex_dic
        }

        return JsonResponse(dic)


# 申请审核
@token.logging_check('POST')
def apply_examine(request):
    if request.method == 'POST':
        user = request.user
        qq = user.qq
        title = request.POST.get('title')
        res_type = request.POST.get('res_type')
        type_id = request.POST.get('type_id')
        if not title:
            dic = {
                'code': 10235,
                'error': '标题不能为空'
            }
            return JsonResponse(dic)
        if not res_type:
            dic = {
                'code': 10236,
                'error': '资源类型不能为空'
            }
            return JsonResponse(dic)
        if not type_id:
            dic = {
                'code': 10237,
                'error': '资源ID不能为空'
            }
            return JsonResponse(dic)
        if res_type not in ['occ', 'cos', 'cou', 'res']:
            dic = {
                'code': 10238,
                'error': '资源类型不正确'
            }
            return JsonResponse(dic)
        try:
            type_id = int(type_id)
        except Exception as e:
            dic = {
                'code': 10240,
                'error': '资源类型不正确'
            }
            return JsonResponse(dic)
        try:
            ExamineRes.objects.create(qq=qq, title=title, res_type=res_type, type_id=type_id)
        except Exception as e:
            dic = {
                'code': 10239,
                'error': '审核提交失败'
            }
            return JsonResponse(dic)
        if res_type == 'occ':
            res = Occ.objects.filter(id=type_id)
        elif res_type == 'cos':
            res = CourSeries.objects.filter(id=type_id)
        elif res_type == 'cou':
            res = Cour.objects.filter(id=type_id)
        else:
            res = Res.objects.filter(id=type_id)

        if not res:
            dic = {
                'code': 10241,
                'error': '当前资源不存在'
            }
            return JsonResponse(dic)
        res[0].audit = '审'
        res[0].save()
        return JsonResponse({'code': 200})


# 审核
@token.user_check('POST')
def examine_adopt(request):
    if request.method == 'POST':
        if request.user_type != 1:
            dic = {
                'code': 10243,
                'error': '非审核管理员'
            }
            return JsonResponse(dic)
        res_type = request.POST.get('res_type')
        type_id = request.POST.get('type_id')
        cla = request.POST.get('cla')
        if not res_type:
            dic = {
                'code': 10244,
                'error': '资源类型不能为空'
            }
            return JsonResponse(dic)
        if not type_id:
            dic = {
                'code': 10245,
                'error': '资源ID不能为空'
            }
            return JsonResponse(dic)
        if not cla:
            dic = {
                'code': 10249,
                'error': '审核类型不正确'
            }
            return JsonResponse(dic)
        try:
            type_id = int(type_id)
        except Exception as e:
            dic = {
                'code': 10246,
                'error': '资源ID不正确'
            }
            return JsonResponse(dic)
        exs = ExamineRes.objects.filter(res_type=res_type, type_id=type_id)
        if not exs:
            dic = {
                'code': 10247,
                'error': '当前资源审核请求不存在'
            }
            return JsonResponse(dic)
        if res_type == 'occ':
            res = Occ.objects.filter(id=type_id)
        elif res_type == 'cos':
            res = CourSeries.objects.filter(id=type_id)
        elif res_type == 'cou':
            res = Cour.objects.filter(id=type_id)
        else:
            res = Res.objects.filter(id=type_id)

        if not res:
            dic = {
                'code': 10248,
                'error': '当前资源不存在'
            }
            return JsonResponse(dic)
        if cla == '1':
            res[0].audit = '通'
        elif cla == '0':
            res[0].audit = '不'
        res[0].save()
        exs.delete()
        return JsonResponse({'code': 200})


# 资源区
def res_area(request):
    if request.method == 'GET':
        cla = request.GET.get('cla')
        res_type = request.GET.get('res_type')
        ye = request.GET.get('ye', 1)
        if not cla:
            dic = {
                'code': 10250,
                'error': '排序方式不能为空'
            }
            return JsonResponse(dic)
        if not res_type:
            dic = {
                'code': 10251,
                'error': '资源类型不能为空'
            }
            return JsonResponse(dic)
        try:
            ye = int(ye)
        except Exception as e:
            dic = {
                'code': 10255,
                'error': '分页类型不正确'
            }
            return JsonResponse(dic)

        if res_type == 'occ':
            res = Occ
        elif res_type == 'cos':
            res = CourSeries
        elif res_type == 'cou':
            res = Cour
        elif res_type == 'res':
            res = Res
        else:
            dic = {
                'code': 10253,
                'error': '资源类型不正确'
            }
            return JsonResponse(dic)

        rea = res.objects.filter(overt=True, audit='通')
        if cla == 'newe':
            re = rea.order_by('-create_date')
        elif cla == 'coll':
            re = rea.order_by('-collection')
        else:
            dic = {
                'code': 10254,
                'error': '排序方式不正确'
            }
            return JsonResponse(dic)
        paginator = Paginator(re, 8)
        pag = paginator.page(ye)
        res_list = []
        for pa in pag:
            dic = {
                'id': pa.id,
                'name': pa.user.name,
                'title': pa.title,
                'cover': str(pa.cover),
                'collection': pa.collection
            }
            res_list.append(dic)
        pag_dic = paging(ye, paginator.num_pages)
        dic = {
            'code': 200,
            'data': res_list,
            'paging': pag_dic
        }

        return JsonResponse(dic)


# 获取用户状态
@token.user_check('GET')
def get_user_type(request):
    if request.method == 'GET':
        if request.user_type == 0:
            if_login = False
        else:
            if_login = True
        dic = {
            'code': 200,
            'data': if_login
        }
        return JsonResponse(dic)


# 分页
def paging(z, h):
    zong = 17
    if h <= zong:
        return {'q': 1, 'z': z, 'h': h}
    else:
        zh = int(zong/2) + 1
        if z <= zh:
            return {'q': 1, 'z': z, 'h': zong}
        elif (z + zh - 1) < h:
            return {'q': z - zh + 1, 'z': z, 'h': z + zh - 1}
        else:
            return {'q': h-zong+1, 'z': z, 'h': h}







