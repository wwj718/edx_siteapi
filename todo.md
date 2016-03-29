#入侵的艺术
利用python的动态特性，去非侵入式地改造系统。  

###添加装饰器
使用装饰器去hack原生的函数，将其定制为需要的功能:

*  import 到siteapi中，然后使用装饰器包装它：some_view = some_wrapper(some_view),之后使用view指向这个新的view，如果把requees和认证的的机制搞清楚会更强大

关于装饰器:[元编程](http://python3-cookbook.readthedocs.org/zh_CN/latest/chapters/p09_meta_programming.html)


###解除一个装饰器
假设装饰器是通过 @wraps (参考9.2小节)来实现的，那么你可以通过访问 __wrapped__ 属性来访问原始函数

参考： [解除一个装饰器](http://python3-cookbook.readthedocs.org/zh_CN/latest/c09/p03_unwrapping_decorator.html)

###定义一个带参数的装饰器
参考:[定义一个带参数的装饰器](http://python3-cookbook.readthedocs.org/zh_CN/latest/c09/p04_define_decorator_that_takes_arguments.html)

###使用mock之类的技术去更改数据流

###弄清request的细节
###弄清认证的细节
###弄清cookie和session的细节

###url的动态性
动态属性开启：
核心包括:

```
if settings.WIKI_ENABLED:
urlpatterns += ()
```
