#!/usr/bin/env python
# encoding: utf-8
from .models import CourseTab
from django.core.exceptions import ObjectDoesNotExist
def get_tab_list(course_id):
    """
    Usage
    from siteapi.course_extra import get_tab_list
    tab_list=get_tab_list(course.id.to_deprecated_string())
    """
    try:
        course_tab = CourseTab.objects.get(course_id=course_id)
        tab_list = course_tab.tab_list
    except ObjectDoesNotExist:
        tab_list = "all"
    return tab_list

