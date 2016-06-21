from django.contrib import admin

from blog.models import Article,Category,Tag 


admin.site.register(Article)
admin.site.register(Category)

admin.site.register(Tag)

