#!/usr/bin/env python
# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError
from django.db import models
#from placeholders import *
import os

class Command(BaseCommand):
     def handle(self, *args, **options):
         print 'hello,edx!'
