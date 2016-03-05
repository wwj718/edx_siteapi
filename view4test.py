#!/usr/bin/env python
# encoding: utf-8

#使用装饰器 改变return
def change_response_content(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result['wwj'] = "It's ok."
        #from ipdb import set_trace;set_trace()
        result.content = u"被我修改啦"
        return result
    return wrapper

import json
def tran2json(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result.mimetype='application/json'
        content_dict = {"content":result.content,"view":"tran2json"}
        result.content=json.dumps(content_dict),
        result['wwj'] = "It's ok."
        #from ipdb import set_trace;set_trace()
        return result
    return wrapper




from django.http import HttpResponse

#@dec
@tran2json
def hello_world(request):
    return HttpResponse("Hello World")

