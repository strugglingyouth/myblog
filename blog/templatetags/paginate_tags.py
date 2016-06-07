#!/usr/bin/env python
# coding=utf-8

from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

def get_left(current_page, left, num_pages):
    """
        当前页为最大值时，取左边2个，否则包含自己在内取三个
    """
    if current_page == 1:
        return []
    elif current_page == num_pages:
        l = [i - 1 for i in range(current_page, current_page - left, -1) if i - 1 > 1]
        l.sort()
        return l
    l = [i for i in range(current_page, current_page - left, -1) if i > 1 ]
    l.sort()
    return l
        
def get_right(current_page, right, num_pages):
    """
        取右边两个不包含自己
    """
    if current_page == num_pages:
        return []
    return [i + 1 for i in range(current_page, current_page + right - 1) if i < num_pages - 1]
        










