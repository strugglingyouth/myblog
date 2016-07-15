# coding:utf-8
"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required


from blog import views 


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^blog/article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^blog/category/(?P<cate_id>\d+)$', views.CategoryView.as_view(), name='category'),
    # 标签对应的 url
    url(r'^tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    # 文章归档对应的 url
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', views.ArchiveView.as_view(), name='archive'),
    # 评论对应的 URL
    url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),

    url(r'^feeds/$', views.RssFeed(), name="rss"),

#    url(r'accounts/login/$', 'django.contrib.auth.views.login', {'template_name': login.html}),

    # 登录页面
#    url(r'^login/$', views.login, name="login"),

    #登出
#    url(r'logout/$', views.logout, name="logout"),

]
