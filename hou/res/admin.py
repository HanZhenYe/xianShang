from django.contrib import admin
from .models import *


# 职业信息显示
class OccAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'overt', 'audit', 'collection']
    list_display_links = ['title']
    search_fields = ['title']


# 课程系列信息显示
class CourSeriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'overt', 'audit', 'collection']
    list_display_links = ['title']
    search_fields = ['title']


# 课程信息显示
class CourAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'overt', 'audit', 'collection']
    list_display_links = ['title']
    search_fields = ['title']


# 资源信息显示
class ResAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'overt', 'audit', 'collection']
    list_display_links = ['title']
    search_fields = ['title']


# 资源平台信息表
class PlatfromAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create_date', 'quantity']
    list_display_links = ['name']
    search_fields = ['name']


# 收藏表
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'res_type', 'type_id']
    list_display_links = ['id']
    search_fields = ['type_id']


# 待审核表
class ExamineResAdmin(admin.ModelAdmin):
    list_display = ['id', 'qq', 'title', 'res_type', 'type_id']
    list_display_links = ['qq']
    search_fields = ['qq', 'title']


admin.site.register(Occ, OccAdmin)
admin.site.register(CourSeries, CourSeriesAdmin)
admin.site.register(Cour, CourAdmin)
admin.site.register(Res, ResAdmin)
admin.site.register(Platfrom, PlatfromAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(ExamineRes, ExamineResAdmin)

