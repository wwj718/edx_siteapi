#!/usr/bin/env python
# encoding: utf-8
from django.db import models


class CourseTab(models.Model):
    course_id = models.CharField(max_length=100, primary_key=True )
    tab_list = models.CharField(max_length=200)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

#class CourseTab():
#    pass
