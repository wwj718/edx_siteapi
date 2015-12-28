#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.models import User
from student.models import UserProfile
from student.models import  Registration

def create_user(username,password,email,name):
        user = User(username=username,
                email=email,
                is_active=True,
                )
        user.set_password(password)
        user.save()
        registration = Registration()
        registration.register(user)
        profile = UserProfile(user=user)
        profile.name = name
        profile.save()

def delete_user(username):
    user = User.objects.get(username=username)
    user.is_active=False
    user.email = "deactive___"+user.email
    #profile = UserProfile.objects.get(user=user)
    #profile.delete()
    user.save()
