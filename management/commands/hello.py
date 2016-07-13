#!/usr/bin/env python
# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError
from django.db import models
#from placeholders import *
import os

class Command(BaseCommand):
    help = u'批量导入用户'
    def handle(self, *args, **options):
        #print 'hello,edx!'
        self.stdout.write(u"导入成功!", ending='')
