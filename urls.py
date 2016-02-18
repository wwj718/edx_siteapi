#!/usr/bin/env python
# encoding: utf-8

import views
#from rest_framework.routers import DefaultRouter
from django.conf.urls import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
    url(r'^user', views.user),
    #url(r'^course_enrollment',views.course_enrollment),

    #todo
    #url(r'^grade/courses/{}/username/(?P<username>\w+)'.format(settings.COURSE_ID_PATTERN), views.grade),
    #url(r'^video_outlines', views.video_outlines),
    #url(r'^learning_record', views.learning_record),
    #access
    #url(r'^access', views.access),


    ############
    #即将丢弃
    #url(r'^users', views.users),
)

