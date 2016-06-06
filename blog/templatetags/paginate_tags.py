#!/usr/bin/env python
# coding=utf-8

from django import template
from django.core.paginate import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()

@register.simple_tag(takes_context=True)
def paginate(context, object_list, page_count):
    left = 3
    right = 3
    paginator = Paginator(object_list, page_count)
    page = context['request'].GET.get('page')

    try:
        object_list = paginator.page(page)
        context['current_page'] = int(page)
        pages = get_left(context['current_page'], left, paginator.num_pages) + get_right(context['current_page'], right, paginator.num_pages)

    except PageNotAnInteger:
        # page 不是整数则返回第一页
        object_list = paginator.page(1)
        context['current_page'] = 1
        pages = get_right(context['current_page'], right, paginator.num_pages)
    except EmptyPage:
        # page 为空则返回最后一页
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages
        pages = get_left(context['current_page'], left, paginator.num_pages)

    context['article_list'] = object_list
    context['pages'] = pages
    context['last_page'] = paginator.num_pages
    context['first_page'] = 1

    try:
        context['pages_first'] = pages[0]
        context['page_last'] = pages[-1] + 1
    except IndexError:
        context['pages_first'] = 1
        context['pages_last'] = 2
    return ''

def get_left():
    pass

def get_right():
    pass



