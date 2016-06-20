# coding:utf-8

from django.shortcuts import render

from django.views.generic import ListView,DetailView
from blog.models import Article, Category
import markdown2


class IndexView(ListView):  
    """
        首页视图函数，继承 ListView ，展示从数据库中获取的文章列表   
    """
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        """
            重写 get_queryset 方法，取出发表的文章并转换文章格式
        """
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    """
        文章详情页
    """

    model = Article
    template_name = 'blog/detail.html'
    context_object_name = "article"
    # 传递到模板文件中的变量

    pk_url_kwarg = 'article_id'
    # 在 urlpattern 中定义的


    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()  #重写 get_object
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj


class CategoryView(ListView):
    """
        分类视图，点击某个分类，展示分类下的所有文章
    """

    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'],status='p')

        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(ListView):
    """
        标签云，获取标签下的文章
    """
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        """
            获取指定标签下的全部文章
        """
        
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tar_id'] = Tag.objects.all().order_by('name')
        return super(TagView, self).get_context_data(**kwargs)







