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
from serializers import UserSerializer,TabSerializer,EnrollmentSerializer
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

class Course(APIView):
    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAdminUser,)
    def post(self, request, format=None):
        #look at [expect_json](https://github.com/edx/edx-platform/blob/named-release/dogwood.rc/common/djangoapps/util/json_request.py#L34)
        request.META["CONTENT_TYPE"]="application/json"
        request_data = request.DATA
        course_id = "course-v1:{org}+{number}+{run}".format(org=request_data.get("org","defaultOrg"),number=request_data.get("number","defaultNumber"),run=request_data.get("run","defaultRun"))
        #return Response({"message": "user2 get","user":str(request.user)})
        try:
            data = create_or_rerun_course(request)
        except:
            pass
        return Response({"message": "course ok","course_id":course_id,"request_data":request_data,"user":str(request.user)})

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
        serializer = TabSerializer(data=request.DATA)
        if  not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            #serializer.data
            request_data = serializer.data
            course_id = request_data.get("course_id","")
            tab_list= request_data.get("tab_list","")
            result = self.change_tab_list(course_id,tab_list)
            return Response({"message":result,"request_data":request_data,"user":str(request.user)})

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
        serializer = EnrollmentSerializer(data=request.DATA)
        if  not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = request.DATA
        username = data["username"]
        course_id = data["course_id"]
        message = "ok"
        succceed = self._course_enroll(username,course_id)
        message = "ok" if succceed else "error"
        return Response({"message": message, "data": data})
    def delete(self, request, format=None):
        #这种资源命名为什么呢，抽象的资源，就叫用户注册的课程,接受用户和课程名
        serializer = EnrollmentSerializer(data=request.DATA)
        if  not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = request.DATA
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

'''
class Tab(APIView):
    #最终方案
    #采用js来做吧
    #或者css？下载云端然后使用sed来插入course.html里？
    #使用jquery，移除
    #$("a[href$=course_wiki]").hide()
    #/instructor,/progress,/forum,/info,/courseware
    #包括新的按钮也这样做

    authentication_classes = (SessionAuthentication,OAuth2Authentication,)
    permission_classes = (IsAdminUser,)
    def get_tab_info(self, request, format=None):
        #/edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py cms --settings aws edit_course_tabs --course course-v1:json_org+json_number100+json_run3
        #tab_info_sh = edxapp_python("/edx/app/edxapp/edx-platform/manage.py","cms","--settings","aws","edit_course_tabs","--course","course-v1:json_org+json_number100+json_run3")
        request_data = request.DATA
        tab_info =subprocess.check_output(["/edx/bin/python.edxapp","/edx/app/edxapp/edx-platform/manage.py","cms","--settings","aws","edit_course_tabs","--course",request_data.get("course_id")])
        return Response({"message": tab_info,"request_data":request_data,"user":str(request.user)})

    def post(self, request, format=None):
        #get 也用post吧
        request_data = request.DATA
        course_id = request_data.get("course_id")
        tab_num = request_data.get("tab_num","")
        if not tab_num:
            return self.get_tab_info(request)

        #--insert <tab-number> <type> <name>, e.g. 2 "course_info" "Course Info"
        # [{u'type': u'courseware'}, {u'type': u'course_info', u'name': u'Course Info'}, {u'type': u'textbooks'},
        # {u'type': u'discussion', u'name': u'Discussion'}, {u'type': u'wiki', u'name': u'Wiki'},
        # {u'type': u'progress', u'name': u'Progress'}]
        #Tab of type 'progress' appears 2 time(s). Expected maximum of 1 time(s).
        tab_type = request_data.get("tab_type","")
        name = request_data.get("name","")
        tab_info = subprocess.Popen("/edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py cms --settings aws edit_course_tabs --course {course_id} --insert {tab_num} {tab_type} {name}".format(course_id=course_id,tab_num=tab_num,tab_type=tab_type,name=name),stdin=subprocess.PIPE, shell=True)
        tab_info.communicate(b"y")
        return Response({"message": "create tab ok","request_data":request_data,"user":str(request.user)})

    def delete(self, request, format=None):
        request_data = request.DATA
        #取消确认
        course_id = request_data.get("course_id")
        tab_num = request_data.get("tab_num")
        tab_info = subprocess.Popen("/edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py cms --settings aws edit_course_tabs --course {course_id} --delete {tab_num}".format(course_id=course_id,tab_num=tab_num),stdin=subprocess.PIPE, shell=True)
        tab_info.communicate(b"y")
        #tab_info =subprocess.check_output(["/edx/bin/python.edxapp","/edx/app/edxapp/edx-platform/manage.py","cms","--settings","aws","edit_course_tabs","--course","course-v1:json_org+json_number100+json_run3","--delete","4"])
        #look at [expect_json](https://github.com/edx/edx-platform/blob/named-release/dogwood.rc/common/djangoapps/util/json_request.py#L34)
        return Response({"message": "delete {tab_num}".format(tab_num=tab_num),"user":str(request.user)})
'''


