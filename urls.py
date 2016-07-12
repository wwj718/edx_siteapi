#!/usr/bin/env python
# encoding: utf-8

import views
import view4test
#from rest_framework.routers import DefaultRouter
from django.conf.urls import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
    #base class
    url(r'^user$', views.User.as_view()),
    url(r'^course$', views.Course.as_view()),
    #url(r'^course/({})?$'.format(settings.COURSE_ID_PATTERN), views.Course.as_view()),
    #url(r'^tab$', views.Tab.as_view()),
    url(r'^enrollment$', views.Enrollment.as_view()),
    url(r'^qiniu$', views.Qiniu.as_view()),
    #url(r'^course_enrollment',views.course_enrollment),
    url(r'^access$', views.Access.as_view()),
    #for test
    url(r'^hello_world$', view4test.hello_world),
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

