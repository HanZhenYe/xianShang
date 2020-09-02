"""qian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from . import views
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    url(r'^user/login$', views.login),
    url(r'^index$', views.index),
    url(r'^user$', views.geren),
    url(r'^occ/admin/(\d+)', views.occ_admin),
    url(r'^courseries/admin/(\d+)', views.courseries_admin),
    url(r'^cour/admin/(\d+)', views.cour_admin),
    url(r'^res/admin/(\d+)', views.res_admin),
    url(r'^res/occ/(\d+)', views.get_occ),
    url(r'res/cos/(\d+)', views.get_cour_series),
    url(r'^res/cou/(\d+)', views.get_cour),
    url(r'^res/res/(\d+)', views.get_res),
    url(r'^examine$', views.examine),
    url(r'^res/area$', views.res_ares),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
