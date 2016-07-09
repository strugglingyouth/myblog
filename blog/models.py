# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from collections import defaultdict


class ArctileManager(models.Manager):
    """
        继承manager并为其添加一个 archive 方法
    """
    
    def archive(self):
        date_list = Article.objects.datetimes('created_time', 'month', order='DESC')
        
        date_dict = defaultdict(list)  #将字典中的values默认常见为list的实例
        for d in date_list:
            date_dict[d.year].append(d.month)

        return sorted(date_dict.items(), reverse=True)    

class time_stamp(models.Model):
    """
        抽象基类
    """
    # auto_now_add 一次产生  auto_now 每次动作都会更新
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    class Meta:
        abstract = True


class Article(models.Model):
    """
        文章结构
    """
    STATUS_CHOICES = (
            ('d','Draft'),
            ('p','Published'),
            ('w','Withdrawn'),  #撤回
        )
    title = models.CharField('标题',max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    abstract = models.CharField('摘要', max_length=54, blank=True, null=True, help_text="可选，为空则提取前54个字符")
    views = models.PositiveIntegerField('浏览量',default=0)
    likes = models.PositiveIntegerField('点赞数',default=0)
    topped = models.BooleanField('置顶', default=False)
    category = models.ForeignKey('Category', verbose_name='分类',null=True,on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签云', blank=True)
    #author = models.ForeignKey(User,'作者')

    def __str__(self):
        return self.title
    def __unicode(self):
        return self.title

    objects = ArctileManager()

    class Meta:
        ordering = ['-last_modified_time']

    # 为 Comment 的 FormView 提供的一个获取 url 的方法
    def get_obsolute_url(self):
        # reverse 解析 blog:detail 视图对应的 url  
        return reverse('blog:detail', kwargs={'article_id': self.pk})


class Category(models.Model):
    """
        目录分类
    """

    name = models.CharField('类名',max_length=20)
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间',auto_now=True)

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Tag(models.Model):
    """
        标签云
    """

    name = models.CharField('标签名', max_length=20) 
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now_add=True)

    def __str__(self):
        return self.name 
    def __unicode__(self):
        return self.name 


class BlogComment(models.Model):
    """
        评论信息
    """
    user_name = models.CharField('评论者名字', max_length=100)
    user_email = models.EmailField('评论者邮箱', max_length=255)
    body = models.TextField('评论内容')
    created_time = models.DateTimeField('发表评论时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论文章', on_delete=models.CASCADE)
    website = models.URLField('站点信息')  #检查 url 可用性

    def __str__(self):
        return self.body[:20]  

    def __unicode__(self):
        return self.body[:20]







