# coding:utf-8

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import BlogCommentForm
from django.views.generic import ListView, DetailView, FormView, TemplateView
from blog.models import Article, Category, Tag, BlogComment
from django.contrib.syndication.views import Feed
from django.http import HttpResponse
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

        # 使用自定义的 manager ，调用 archive 方法，
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
        """ 
            错误处理，请求文章不存在
        """
        try:
            obj = super(ArticleDetailView, self).get_object()  #重写 get_object
            obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        except Exception as e:
            obj="Article  is NotFound!"
            return obj
        return obj  

    # 增加 form 到 context
    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = self.object.blogcomment_set.all()  #获取评论
        kwargs['form'] = BlogCommentForm()
        kwargs['comment_count'] = self.object.blogcomment_set.count() #获取评论数量
        return super(ArticleDetailView, self).get_context_data(**kwargs)


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

class ArchiveView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    
    
    def get_queryset(self): 
        # 将从 url 传入的参数year 和 month 转换为 int
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])

        article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

class CommentPostView(FormView):
    form_class = BlogCommentForm  #指定使用的 form
    template_name = 'blog/detail.html'  #指定使用的模板文件

    def form_valid(self, form):
        """
            提交的数据合法
        """
        #get_object_or_404() 函数需要一个 Django 模型类作为第一个参数以及 一些关键字参数，它将这些参数传递给模型管理器中的 get() 函数。 若对象不存在时就抛出 Http404 异常。
        # 首先根据 url 传入的文章 id ，获取相应的文章
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])


        comment = form.save(commit=False)   #实例化一个 comment 对象，但是不保存评论
        comment.article = target_article    # 为 comment 关联一个文章,即添加一个属性
        comment.save()                      # 保存评论的内容

        # 评论完成后返回到被评论的文章页面, get_obsolute_url 是 Article 新增的一个方法方便,获取文章对用的 url
        self.success_url = target_article.get_absolute_url()  
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        """
            提交的数据不合法
        """
        
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        
        # 不保存评论，返回原来的文章页面
        return render(self.request, 'blog/detail.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.blogcomment_set.all(),
            #'comment_count': target_article.blogcomment_set.count(),
        })

class RssFeed(Feed):
    """
        RSS 订阅
    """
    title = "RSS Feed - article"
    link = "/feeds/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by("-created_time")
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.abstract
    def item_pubdate(self, item):
        return item.created_time

class LoginView(TemplateView):
    """
        登录页面
    """
    template_name = 'blog/login.html'
    def form_valid(self):
        pass
    def get_context_data(self, **kwargs):
        pass

def Github(request):
    """
        Github
    """
    return HttpResponseRedirect('https://github.com/strugglingyouth')


class AboutView(ListView):
    """
        About me
    """
    template_name = "blog/about.html"
    context_object_name = "article_about_me"

    def get_queryset(self):
        article_about_me = Article.objects.filter(category__name='about',status='w')
        return article_about_me   















