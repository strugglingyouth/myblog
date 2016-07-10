#!/usr/bin/env python
# coding:utf-8

from django import forms
from .models import Article, BlogComment


class BlogCommentForm(forms.ModelForm):
    """
        评论表单
    """
    class Meta:
        """
            指定一些 Meta 选项以改变 form 被渲染后的样式
        """
        model = BlogComment #指定 form 关联的 model
        # 需要渲染的字段
        fields = ['user_name', 'user_email', 'body', 'website']
        
        widgets = {
            # 为要渲染的字段添加 css 样式
            # 例如 user_name 渲染后的html组件如下：
            # <input type="text" class="form-control" placeholder="Username" aria-describedby="sizing-addon1">


            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "请输入昵称",
                'aria-describedby': "sizing-addonl",
            }),
            'user_email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入邮箱',
                'aria-describedby': 'sizing-addonl',
            }),
            'website': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入网址',
                'aria-describedby': 'sizing-addonl',
            }),
            'body': forms.Textarea(attrs={
                'placeholder': '说点什么吧...',
            }),

        }
        
