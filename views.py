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
#注意当前rest框架版本为2.3.14，文档为：[rest-framework-2-docs](http://tomchristie.github.io/rest-framework-2-docs/)

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

#改为类的写法
# 使用序列化来验证参数
from rest_framework.views import APIView
from serializers import UserSerializer
from rest_framework import status
class User2(APIView):
    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAdminUser,)
    def get(self, request, format=None):
        return Response({"message": "user2 get","user":str(request.user)})
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            #serializer.data
            message = "from User2"
            return Response({"message": message, "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


