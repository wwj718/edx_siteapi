#!/usr/bin/env python
# encoding: utf-8


from rest_framework import serializers
from .utils import user_exist,check_course_id
from .models import CourseTab
import re
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100,required=False)
    age = serializers.IntegerField(max_value=100, min_value=0,required=False)


class CourseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    org = serializers.CharField(max_length=100)
    number = serializers.CharField(max_length=100)
    run = serializers.CharField(max_length=100)
    course_name = serializers.CharField(max_length=100)

    def validate(self, data):
        username_or_email = data["username"] # 创建者？
        user = user_exist(username_or_email)
        if not user:
            raise serializers.ValidationError(u'用户不存在')
        else:
            return data

class TeacherSerializer(serializers.Serializer):
    course_id = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    def validate(self, data):
        course_id = data["course_id"]
        username_or_email = data["username"]
        if not user_exist(username_or_email):
            raise serializers.ValidationError(u'用户不存在')
        if not check_course_id(course_id):
            raise serializers.ValidationError(u'course_id不存在')
        return data


class TabSerializer(serializers.Serializer):
    course_id = serializers.CharField(max_length=100)
    tab_list = serializers.CharField(max_length=100)
    def validate(self, data):
        course_id = data["course_id"]
        if not check_course_id(course_id):
            raise serializers.ValidationError(u'course_id不存在')
        return data

class EnrollmentSerializer(serializers.Serializer):
    course_id = serializers.CharField(max_length=100)
    username_list = serializers.CharField(max_length=100)
    def validate(self, data):
        course_id = data["course_id"]
        username_or_email = data["username_list"]
        #for username in username_or_email.spilt(","): #切隔,
        for username in re.split(u',| |，', username_or_email): # 切割非单词字符，除了email
            if not user_exist(username):
                # 检验用户是否注册
                raise serializers.ValidationError(u'{}用户不存在'.format(username))
        if not check_course_id(course_id):
            raise serializers.ValidationError(u'course_id不存在')
        return data
