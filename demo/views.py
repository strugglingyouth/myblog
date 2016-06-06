# coding:utf-8

from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,ListView,DetailView

from blog.models import Article


class ProtectedView(TemplateView):
    Template_name = 'blog/about.html'

    @method_decorator(login_required)  #装饰基于类的视图的每个实例
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)



class Content(ListView):
    model = Article
    template_name = 'blog/about.html'
    
    def get_context_data(self, **kwargs):
        context = super(Content, self).get_context_data(**kwargs)

        context['article_list'] = Article.objects.filter(id=3)
        return context

class Content_1(ListView):
   # context_object_name = 'context'
   # queryset = Article.objects.all()
    template_name = 'blog/about.html'

    def get_queryset(self): #动态过滤
        #self.status = get_object_or_404(Article, name=self.args[0])
        self.status = self.args[0]
        return Article.objects.filter(status=self.status)


def demo(request):
    result = {'demo':'demo'}
    return render(request, 'blog/about.html', result)



