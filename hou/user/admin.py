from django.contrib import admin
from .models import *


# 用户信息显示
class UserAdmin(admin.ModelAdmin):
    list_display = ['qq', 'name', 'age', 'birth_date', 'create_date']
    list_display_links = ['qq']
    search_fields = ['qq', 'name']


# 邮箱验证表
class EmailYanAdmin(admin.ModelAdmin):
    list_display = ['qq', 'img_code', 'email_code', 'email_time', 'login_shu', 'huo_shu']
    list_display_links = ['qq']
    search_fields = ['qq']


# 审核管理员
class ExamineAdmin(admin.ModelAdmin):
    list_display = ['qq']
    list_display_links = ['qq']
    search_fields = ['qq']


admin.site.register(User, UserAdmin)
admin.site.register(EmailYan, EmailYanAdmin)
admin.site.register(Examine, ExamineAdmin)


