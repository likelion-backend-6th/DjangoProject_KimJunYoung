from django.contrib import admin
from django.db import models
from django import forms

from blog.models import Post, Comment


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'author', 'publish', 'status']
	# prepopulated_fields = {'slug': ('title',)}
	#
	# formfield_overrides = {
	# 	models.DateTimeField: {'widget': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S.%f')},
	# }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'post', 'created', 'active']
	list_filter = ['active', 'created', 'update']
	search_fields = ['name', 'email', 'body']



