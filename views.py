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




#sh env的问题
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

#for create course
import  sys
sys.path.append("/edx/app/edxapp/edx-platform/cms/djangoapps")
from contentstore.views import create_or_rerun_course
#import sh
from subprocess import call
class Course(APIView):
    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAdminUser,)
    def post(self, request, format=None):
        #look at [expect_json](https://github.com/edx/edx-platform/blob/named-release/dogwood.rc/common/djangoapps/util/json_request.py#L34)
        request.META["CONTENT_TYPE"]="application/json"
        print
        '''
        request.json ={}
        request.json["org"]="murp"
        request.json["number"]="mycourse0203"
        request.json["display_name"]="hahaha"
        request.json["run"]="2016_t6"
        '''
        #return Response({"message": "user2 get","user":str(request.user)})
        data = create_or_rerun_course(request)
        return Response({"message": "course ok","user":str(request.user)})

import subprocess

class Tab(APIView):

    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAdminUser,)
    def get(self, request, format=None):
        #edxapp_python = sh.Command("/edx/bin/python.edxapp")
        #/edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py cms --settings aws edit_course_tabs --course course-v1:json_org+json_number100+json_run3
        #tab_info_sh = edxapp_python("/edx/app/edxapp/edx-platform/manage.py","cms","--settings","aws","edit_course_tabs","--course","course-v1:json_org+json_number100+json_run3")
        #tab_info = tab_info_sh()

        tab_info =subprocess.check_output(["/edx/bin/python.edxapp","/edx/app/edxapp/edx-platform/manage.py","cms","--settings","aws","edit_course_tabs","--course","course-v1:json_org+json_number100+json_run3"])
        return Response({"message": tab_info,"user":str(request.user)})

    def delete(self, request, format=None):
        #取消确认
        tab_info = subprocess.Popen("/edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py cms --settings aws edit_course_tabs --course course-v1:json_org+json_number100+json_run3 --delete 4",stdin=subprocess.PIPE, shell=True)
        tab_info.communicate(b"y")
        #tab_info =subprocess.check_output(["/edx/bin/python.edxapp","/edx/app/edxapp/edx-platform/manage.py","cms","--settings","aws","edit_course_tabs","--course","course-v1:json_org+json_number100+json_run3","--delete","4"])
        #look at [expect_json](https://github.com/edx/edx-platform/blob/named-release/dogwood.rc/common/djangoapps/util/json_request.py#L34)
        return Response({"message": "delete 4","user":str(request.user)})

class Grade(APIView):
    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAdminUser,)
    def get(self, request, format=None):
        message = "get Grade"
        return Response({"message": message_,"user":str(request.user)})

class Access(APIView):
    # ok
    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        return Response({"message": "Access ok "})

class Enrollment(APIView):
    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAdminUser,)
    def get(self, request, format=None):
        message = "get Enrollment"
        return Response({"message":message ,"user":str(request.user)})
