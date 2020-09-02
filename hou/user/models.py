from django.db import models


# 用户表
class User(models.Model):
    qq = models.BigIntegerField('QQ', primary_key=True)
    name = models.CharField('用户名', max_length=39)
    age = models.CharField('性别', max_length=3, default='男')
    birth_date = models.DateField('生日', default='2020-1-1')
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    portrait = models.ImageField('头像', upload_to='portrait', null=True)
    token = models.CharField('Token', max_length=600)
    my_occ = models.IntegerField('我的职业', default=0)
    my_cour_series = models.IntegerField('我的系列', default=0)
    my_cour = models.IntegerField('我的课程', default=0)
    my_res = models.IntegerField('我的资源', default=0)
    my_not = models.IntegerField('我的笔记', default=0)
    coll_occ = models.IntegerField('收藏的职业', default=0)
    coll_cour_series = models.IntegerField('收藏的系列', default=0)
    coll_cour = models.IntegerField('收藏的课程', default=0)
    coll_res = models.IntegerField('收藏的资源', default=0)
    coll_not = models.IntegerField('收藏的笔记', default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


# 图片验证地址
class ImgYan(models.Model):
    code = models.CharField('验证码', max_length=12)
    path = models.CharField('图片路径', max_length=100)


# 图片列表
class ImgList(models.Model):
    id = models.IntegerField('id', primary_key=True)
    img_list = models.TextField('图片列表')


# 邮箱验证
class EmailYan(models.Model):
    qq = models.BigIntegerField('qq', primary_key=True)
    img_code = models.CharField('图片验证码', max_length=12)
    email_code = models.IntegerField('邮箱验证码', null=True)
    email_time = models.DateTimeField('验证码获取时间', auto_now=True)
    login_shu = models.IntegerField('登陆次数', default=1)
    huo_shu = models.IntegerField('获取次数', default=1)

    def __str__(self):
        return str(self.qq)

    class Meta:
        db_table = 'email_yan'
        verbose_name = '邮箱'
        verbose_name_plural = verbose_name


# 审核管理员表
class Examine(models.Model):
    qq = models.BigIntegerField('qq', primary_key=True)

    def __str__(self):
        return str(self.qq)

    class Meta:
        db_table = 'examine'
        verbose_name = '审核'
        verbose_name_plural = verbose_name
