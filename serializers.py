#!/usr/bin/env python
# encoding: utf-8


from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100,required=False)
    age = serializers.IntegerField(max_value=100, min_value=0,required=False)
