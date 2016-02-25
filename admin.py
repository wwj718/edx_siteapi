#!/usr/bin/env python
# encoding: utf-8


from django.contrib import admin
from .models import CourseTab
class CourseTabAdmin(admin.ModelAdmin):
    readonly_fields = ("course_id",)
    search_fields = ('course_id','tab_list')
    fields = ('course_id','tab_list')
    list_display = ('course_id','tab_list')

admin.site.register(CourseTab,CourseTabAdmin)
