from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create_yan$', views.create_yan),
    url(r'^yan$', views.get_yan),
    url(r'^img/yan', views.yan_img),
    url(r'^login$', views.login),
    url(r'^geren$', views.geren),
    url(r'^modify$', views.modify)
]
