# -*- coding: utf-8 -*-
__author__ = 'Joanna667'
from django.contrib import admin
from microblog.models import Tag, Article, UserActivation


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('tag__name',)
    ordering = ('pub_date', )
    list_filter = ('pub_date', )

admin.site.register(Tag)
admin.site.register(UserActivation)
admin.site.register(Article, ArticleAdmin)
