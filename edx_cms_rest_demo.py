#!/usr/bin/env python
# encoding: utf-8

from edx_cms_rest import EdXCourse,EdXCmsConnection

mycourse = EdXCourse("edx", "edx101", "2000")
studio = EdXCmsConnection(session="xxx",server="http://studio.exampke.com",csrf="xxx")
studio.create_course(course=mycourse,course_name="test course")
