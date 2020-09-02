from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.get_res),
    url(r'^user/res$', views.user_res),
    url(r'^admin$', views.res_admin),
    url(r'^cour$', views.get_cour),
    url(r'^update$', views.res_update),
    url(r'^index$', views.index),
    url(r'^shou$', views.shou),
    url(r'^examine$', views.examine),
    url(r'^apply/examine$', views.apply_examine),
    url(r'^examine/adopt$', views.examine_adopt),
    url(r'^area$', views.res_area),
    url(r'^user/type$', views.get_user_type)
]
