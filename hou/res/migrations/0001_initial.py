# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-06-03 06:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_type', models.CharField(max_length=10, verbose_name='资源类型')),
                ('type_id', models.IntegerField(verbose_name='资源ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'verbose_name': '收藏',
                'verbose_name_plural': '收藏',
                'db_table': 'collection',
            },
        ),
        migrations.CreateModel(
            name='Cour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='标题')),
                ('synopsys', models.CharField(max_length=360, verbose_name='简介')),
                ('cover', models.ImageField(null=True, upload_to='cover', verbose_name='封面')),
                ('directory', models.TextField(null=True, verbose_name='课程目录')),
                ('overt', models.BooleanField(default=0, verbose_name='是否公开')),
                ('audit', models.CharField(default='未', max_length=3, verbose_name='审核状态')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('collection', models.IntegerField(default=0, verbose_name='收藏')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
                'db_table': 'cour',
            },
        ),
        migrations.CreateModel(
            name='CourSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='标题')),
                ('synopsys', models.CharField(max_length=360, null=True, verbose_name='简介')),
                ('cover', models.ImageField(null=True, upload_to='cover', verbose_name='封面')),
                ('course_list', models.TextField(null=True, verbose_name='课程列表')),
                ('overt', models.BooleanField(default=0, verbose_name='是否公开')),
                ('audit', models.CharField(default='未', max_length=3, verbose_name='审核状态')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('collection', models.IntegerField(default=0, verbose_name='收藏')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'verbose_name': '系列',
                'verbose_name_plural': '系列',
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='ExamineRes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qq', models.IntegerField(verbose_name='qq')),
                ('title', models.CharField(max_length=60, verbose_name='标题')),
                ('res_type', models.CharField(max_length=10, verbose_name='类型')),
                ('type_id', models.IntegerField(verbose_name='资源ID')),
            ],
            options={
                'verbose_name': '待审核',
                'verbose_name_plural': '待审核',
                'db_table': 'examine_res',
            },
        ),
        migrations.CreateModel(
            name='Occ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='标题')),
                ('synopsys', models.CharField(max_length=360, null=True, verbose_name='简介')),
                ('cover', models.ImageField(null=True, upload_to='cover', verbose_name='封面')),
                ('route', models.TextField(null=True, verbose_name='路线')),
                ('overt', models.BooleanField(default=0, verbose_name='是否公开')),
                ('audit', models.CharField(default='未', max_length=3, verbose_name='审核状态')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('collection', models.IntegerField(default=0, verbose_name='收藏')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'verbose_name': '职业',
                'verbose_name_plural': '职业',
                'db_table': 'occ',
            },
        ),
        migrations.CreateModel(
            name='Platfrom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='平台')),
                ('cover', models.ImageField(null=True, upload_to='cover', verbose_name='封面')),
                ('limk', models.CharField(max_length=100, verbose_name='链接')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('quantity', models.IntegerField(default=0, verbose_name='点击数')),
            ],
            options={
                'verbose_name': '平台',
                'verbose_name_plural': '平台',
                'db_table': 'platfrom',
            },
        ),
        migrations.CreateModel(
            name='Res',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='标题')),
                ('synopsys', models.CharField(max_length=360, verbose_name='简介')),
                ('cover', models.ImageField(null=True, upload_to='cover', verbose_name='封面')),
                ('limk', models.CharField(max_length=300, verbose_name='链接')),
                ('overt', models.BooleanField(default=0, verbose_name='是否公开')),
                ('audit', models.CharField(default='未', max_length=3, verbose_name='审核状态')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('collection', models.IntegerField(default=0, verbose_name='收藏')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'verbose_name': '资源',
                'verbose_name_plural': '资源',
                'db_table': 'res',
            },
        ),
    ]
