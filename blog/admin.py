from django.contrib import admin

from blog.models import Article,Category,Tags 


admin.site.register(Article)
admin.site.register(Category)

admin.site.register(Tags)

