#siteapi
将edx视为子系统，为外部提供RESTful风格的api,技术层面采用与open edx原生api一样的机制

官方的既有的api参考这里:[edx-platform-api](http://edx.readthedocs.org/projects/edx-platform-api/en/latest/)

#设计
*  这部分代码组织形式为django app

#功能
*  站点级别的管理
*  用户管理（增删）
*  课程创建
*  成绩查询
*  注册课程x' (xxxxxxxxx为你的access token )
*  http post http://127.0.0.1:5000/siteapi/user username=wwj password=wwj 'Authorization: Bearer xxx'

#在dogwood中使用
```bash
cd /edx/app/edxapp/edx-platform/lms/djangoapps/
sudo git clone -b clean_dogwood https://github.com/wwj718/edx_siteapi "siteapi"
sudo chown edxapp:edxapp siteapi
sudo /edx/bin/pip.edxapp install -r siteapi/requirements.txt
sudo ./siteapi/add_the_app.sh
```

#调试
安装[httpie](https://github.com/jkbrzt/httpie)

###获取access token
[enable Open edX REST APIs](http://blog.just4fun.site/edx-api.html),只要进入/admin,取得有效access token即可

###access
(ps:sessionid和csrftoken到浏览器获取)

http http://127.0.0.1:5000/siteapi/access  "Cookie:sessionid=aaa;csrftoken=bbb" X-CSRFToken:bbb

###create course
*  http post http://127.0.0.1:5000/siteapi/course  "Cookie:sessionid=aaa;csrftoken=bbb" X-CSRFToken:bbb org=json_org number=json_number run=json_run course_name=json_display_name username=wwj

###contral tab
*  http  post http://127.0.0.1:5000/siteapi/tab   tab_list=courseware+info+forum course_id=course-v1:edX+DemoX+Demo_Course username=staff  "AUTHORIZATION: Bearer xxx"

###enrollment
*  http post http://127.0.0.1:5000/siteapi/enrollment course_id=course-v1:edX+DemoX+Demo_Course username=staff "Authorization: Bearer xxx"
*  http delete http://127.0.0.1:5000/siteapi/enrollment course_id=course-v1:edX+DemoX+Demo_Course username=staff "Authorization: Bearer xxx"

###qiniu
http  http://127.0.0.1:5000/siteapi/qiniu "Authorization: Bearer xxx"  (get upload_token)

###调试请求参数
使用`http://httpbin.org/`,原因返回你发送的http请求

*  http post http://httpbin.org/post tab_list=courseware+info+forum "Authorization: Bearer xxx"

#相似项目
*  [pmitros/edx-rest](https://github.com/pmitros/edx-rest/blob/master/src/edxrest.py)
