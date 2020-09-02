from django.shortcuts import render


# 用户登陆页面
def login(request):
    return render(request, 'login.html')


# 首页
def index(request):
    return render(request, 'index.html')


# 个人中心
def geren(request):
    return render(request, 'geren.html')


# 职业管理
def occ_admin(request, n):
    return render(request, 'occ_admin.html')


# 课程系列管理
def courseries_admin(request, n):
    return render(request, 'cour_series_admin.html')


# 课程管理
def cour_admin(request, n):
    return render(request, 'cour_admin.html')


# 资源链接管理
def res_admin(request, n):
    return render(request, 'res_admin.html')


# 获取职业页面
def get_occ(request, n):
    return render(request, 'occ.html')


# 获取课程系列页面
def get_cour_series(request, n):
    return render(request, 'cour_series.html')


# 获取课程页面
def get_cour(request, n):
    return render(request, 'cour.html')


# 获取资源链接页面
def get_res(request, n):
    return render(request, 'res.html')


# 管理界面
def examine(request):
    return render(request, 'examine.html')


# 资源区
def res_ares(request):
    return render(request, 'res_area.html')
