#!/usr/bin/env python
# encoding: utf-8

#encoding: utf-8
#from django.shortcuts import render
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.authentication import SessionAuthentication #,OAuth2Authentication
from rest_framework_oauth.authentication import OAuth2Authentication

# Create your views here.
from rest_framework.response import Response
#######
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .create_users import create_user,delete_user
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
#from django.db import IntegrityError
from django.contrib.auth.models import User

from opaque_keys.edx.locations import SlashSeparatedCourseKey
from student.models import CourseEnrollment
#from instructor.offline_gradecalc import student_grades
#from courseware.courses import get_course_with_access

#注意当前rest框架版本为2.3.14，文档为：[rest-framework-2-docs](http://tomchristie.github.io/rest-framework-2-docs/)


#改为类的写法
# 使用序列化来验证参数
from rest_framework.views import APIView
from serializers import UserSerializer,TabSerializer,EnrollmentSerializer,CourseSerializer
from rest_framework import status
from .edxrest import EdXConnection,EdXCourse
#from ipdb import set_trace


#sh env的问题
class User(APIView):
    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAdminUser,)
    def get(self, request, format=None):
        return Response({"message": "user2 get","user":str(request.user)})
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.data
            message = "from User2"
            return Response({"message": message, "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Course(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)
    def post(self, request):
        #用户已经验证过了，，取得需要的参数
        request_data = request.data
        #serializer = CourseSerializer(data=request.data)
        #course_id = "course-v1:{org}+{number}+{run}".format(org=request_data.get("org","defaultOrg"),number=request_data.get("number","defaultNumber"),run=request_data.get("run","defaultRun"))
        #set_trace()
        serializer = CourseSerializer(data=request.data)
        if  not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            session = request.COOKIES.get('sessionid','')
            csrftoken = request.COOKIES.get('csrftoken','')
            username =  serializer.data.get("username","")
            org =  serializer.data.get("org","defaultOrg")
            number =  serializer.data.get("number","defaultNumber")
            run =  serializer.data.get("run","defaultRun")
            course_name =  serializer.data.get("course_name","defaultCourse_name")
            course = EdXCourse(org,number,run)
            edx_studio = EdXConnection(session=session,server="http://127.0.0.1:8010",csrf=csrftoken)
            result = edx_studio.create_course(course,course_name)
            return Response(result)


from .models import CourseTab
class Tab(APIView):
    # 课程级别的
    # 建个模型，对课程的属性做扩展
    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAdminUser,)
    def change_tab_list(self,course_id,tab_list):
        #result = "change tab ok"
        (course_tab,created) = CourseTab.objects.get_or_create(
                course_id=course_id,
                defaults={'tab_list': tab_list},)
        if not created:
            course_tab.tab_list=tab_list
            course_tab.save()
        return "tab ok"
    def post(self, request, format=None):
        #直接发一个json来说需要什么
        serializer = TabSerializer(data=request.data)
        if  not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            #serializer.data
            request_data = serializer.data
            course_id = request_data.get("course_id","")
            tab_list= request_data.get("tab_list","")
            result = self.change_tab_list(course_id,tab_list)
            return Response({"message":result,"request_data":request_data})

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
    def post(self, request, format=None):
        #使用序列化验证是否合理
        #用户是否存在 是否合理
        serializer = EnrollmentSerializer(data=request.data)
        if  not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        username = data["username"]
        course_id = data["course_id"]
        message = "ok"
        succceed = self._course_enroll(username,course_id)
        message = "ok" if succceed else "error"
        return Response({"message": message, "data": data})
    def delete(self, request, format=None):
        #这种资源命名为什么呢，抽象的资源，就叫用户注册的课程,接受用户和课程名
        serializer = EnrollmentSerializer(data=request.data)
        if  not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        username = data["username"]
        course_id = data["course_id"]
        succceed = self._course_unenroll(username,course_id)
        message = "ok" if succceed else "error"
        return Response({"message": message, "data": data})
    def _course_enroll(self,username,course_id):
        try:
            user = User.objects.get(username=username)
            course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
            CourseEnrollment.enroll(user, course_key)
            #CourseEnrollment.get_or_create_enrollment(user, course_key)
            return True
        except:
            return False
    def _course_unenroll(self,username,course_id):
        try:
            user = User.objects.get(username=username)
            course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
            CourseEnrollment.unenroll(user, course_key)
            return True
        except:
            return False

# 移除七牛了ast实验部分
# 七牛云视频管理组件单独做成一个django app，采用restful接口
