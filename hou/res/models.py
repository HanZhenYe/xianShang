from django.db import models
from user.models import User


# 职业信息表
class Occ(models.Model):
    title = models.CharField('标题', max_length=60)
    synopsys = models.CharField('简介', max_length=360, null=True)
    cover = models.ImageField('封面', upload_to='cover', null=True)
    route = models.TextField('路线', null=True)
    overt = models.BooleanField('是否公开', default=0)
    audit = models.CharField('审核状态', max_length=3, default='未')
    create_date = models.DateField('创建时间', auto_now_add=True)
    update_date = models.DateTimeField('更新时间', auto_now=True)
    collection = models.IntegerField('收藏', default=0)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'occ'
        verbose_name = '职业'
        verbose_name_plural = verbose_name


# 课程系列信息表
class CourSeries(models.Model):
    title = models.CharField('标题', max_length=60)
    synopsys = models.CharField('简介', max_length=360, null=True)
    cover = models.ImageField('封面', upload_to='cover', null=True)
    course_list = models.TextField('课程列表', null=True)
    overt = models.BooleanField('是否公开', default=0)
    audit = models.CharField('审核状态', max_length=3, default='未')
    create_date = models.DateField('创建时间', auto_now_add=True)
    update_date = models.DateTimeField('更新时间', auto_now=True)
    collection = models.IntegerField('收藏', default=0)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'course'
        verbose_name = '系列'
        verbose_name_plural = verbose_name


# 课程信息表
class Cour(models.Model):
    title = models.CharField('标题', max_length=60)
    synopsys = models.CharField('简介', max_length=360)
    cover = models.ImageField('封面', upload_to='cover', null=True)
    directory = models.TextField('课程目录', null=True)
    overt = models.BooleanField('是否公开', default=0)
    audit = models.CharField('审核状态', max_length=3, default='未')
    create_date = models.DateField('创建时间', auto_now_add=True)
    update_date = models.DateTimeField('更新时间', auto_now=True)
    collection = models.IntegerField('收藏', default=0)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'cour'
        verbose_name = '课程'
        verbose_name_plural = verbose_name


# 资源信息表
class Res(models.Model):
    title = models.CharField('标题', max_length=60)
    synopsys = models.CharField('简介', max_length=360)
    cover = models.ImageField('封面', upload_to='cover', null=True)
    limk = models.CharField('链接', max_length=300)
    overt = models.BooleanField('是否公开', default=0)
    audit = models.CharField('审核状态', max_length=3, default='未')
    create_date = models.DateField('创建时间', auto_now_add=True)
    update_date = models.DateTimeField('更新时间', auto_now=True)
    collection = models.IntegerField('收藏', default=0)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'res'
        verbose_name = '资源'
        verbose_name_plural = verbose_name


# 资源平台信息表
class Platfrom(models.Model):
    name = models.CharField('平台', max_length=60)
    cover = models.ImageField('封面', upload_to='cover', null=True)
    limk = models.CharField('链接', max_length=100)
    create_date = models.DateField('创建时间', auto_now_add=True)
    quantity = models.IntegerField('点击数', default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'platfrom'
        verbose_name = '平台'
        verbose_name_plural = verbose_name


# 收藏表
class Collection(models.Model):
    res_type = models.CharField('资源类型', max_length=10)
    type_id = models.IntegerField('资源ID')
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'collection'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name


# 待审核表
class ExamineRes(models.Model):
    qq = models.IntegerField('qq')
    title = models.CharField('标题', max_length=60)
    res_type = models.CharField('类型', max_length=10)
    type_id = models.IntegerField('资源ID')

    def __str__(self):
        return str(self.qq)

    class Meta:
        db_table = 'examine_res'
        verbose_name = '待审核'
        verbose_name_plural = verbose_name

