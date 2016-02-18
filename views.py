#!/usr/bin/env python
# encoding: utf-8

#encoding: utf-8
from django.shortcuts import render
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.authentication import SessionAuthentication,OAuth2Authentication
# Create your views here.
from rest_framework.response import Response
#######
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .create_users import create_user,delete_user
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.db import IntegrityError
from django.contrib.auth.models import User

from opaque_keys.edx.locations import SlashSeparatedCourseKey
from student.models import CourseEnrollment
from instructor.offline_gradecalc import student_grades
from courseware.courses import get_course_with_access

#Todo 改为基于类的写法

@api_view(['GET', 'POST','DELETE'])
@authentication_classes((SessionAuthentication,OAuth2Authentication))
@permission_classes((IsAdminUser, ))
def user(request):
    if request.method == 'GET':
        return Response({"message": "user get","user":str(request.user)})
    if request.method == 'POST':
        data = request.DATA
        #验证data的合法性 data["user"] 是一个字典
        user = data
        #message = "got it"
        #message = _create_user(user)
        message = "#_create_user"
        #创建用户
        return Response({"message": message, "data": data})
    if request.method == 'DELETE':
        data = request.DATA
        user = data
        #username = user["username"]
        message = _delete_user(user)
        #print user["username"]
        #message = "#_delete_user"
        return Response({"message": message, "data": data})


