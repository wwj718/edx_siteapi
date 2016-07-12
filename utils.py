#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import User
from opaque_keys.edx.keys import CourseKey
#from xmodule.contentstore.django import contentstore
from opaque_keys import InvalidKeyError
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xmodule.modulestore.django import modulestore

def user_exist(username_or_email):
        try:
            if '@' in username_or_email:
                user = User.objects.get(email=username_or_email)
            else:
                user = User.objects.get(username=username_or_email)
            return user
        except User.DoesNotExist:
            return False

def check_course_id(course_id):
        try:
            course_key = CourseKey.from_string(course_id)
        except InvalidKeyError:
            try:
                course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
            except InvalidKeyError:
                return False
        if modulestore().get_course(course_key):
            return True
        return False
