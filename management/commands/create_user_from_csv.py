#!/usr/bin/env python
# encoding: utf-8
from optparse import make_option
from django.core.management.base import BaseCommand

from student.forms import AccountCreationForm
from student.models import create_comments_service_user
from student.views import _do_create_account, AccountValidationError
from track.management.tracked_command import TrackedCommand
# 解析csv
import unicodecsv  # utf-8 ,也可以用pandas:


def create_user(username, password, email, name):
    form = AccountCreationForm(data={
        'username': username,
        'email': email,
        'password': password,
        'name': name,
    },
                               tos_required=False)
    try:
        user, _, reg = _do_create_account(form)
        reg.activate()
        reg.save()
        #create_comments_service_user(user) #这会促发网络请求
        return user
    except AccountValidationError as e:
        print e.message


# wget https://raw.githubusercontent.com/edx/edx-platform/named-release/dogwood.rc/common/djangoapps/student/management/commands/create_user.py
class Command(TrackedCommand):
    help = """
    example:
        # Enroll a user test@example.com into the demo course
        # The username and name will default to "test"
        sudo -u www-data /edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py lms create_user_from_csv --help --settings devstack
        sudo -u www-data /edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py lms create_user_from_csv --csv /edx/app/edxapp/edx-platform/lms/djangoapps/siteapi/student.csv --settings devstack
    """
    help = u"批量导入用户"
    option_list = BaseCommand.option_list + (
        make_option('-c', '--csv', #采用绝对路径
                    metavar='CSV',
                    dest='csv',
                    default=None,
                    help=u'用户注册表'),
        )

    def handle(self, *args, **options):
        csv = options['csv']
        with open(csv) as f:
            f_csv = unicodecsv.DictReader(f, encoding='utf-8')
            for item in f_csv:
                print item[u"姓名"]
                username = item[u"学号"]
                email = item[u"email"]
                name = item[u"姓名"]
                password = username
                create_user(username, password, email, name)
        # 缺乏读写csv的技巧,next和边界，按header读取
        # http://python3-cookbook.readthedocs.io/zh_CN/latest/c06/p01_read_write_csv_data.html
