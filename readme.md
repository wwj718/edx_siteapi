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
*  注册课程(xxxxxxxxx为你的access token )
*  http post http://127.0.0.1:5000/siteapi/user username=wwj password=wwj 'Authorization: Bearer xxx'

#在dogwood中使用
```bash
cd /edx/app/edxapp/edx-platform/lms/djangoapps/
sudo git clone  https://github.com/wwj718/edx_siteapi "siteapi"
sudo chown edxapp:edxapp siteapi
sudo ./siteapi/add_the_app.sh
/edx/bin/python.edxapp  /edx/app/edxapp/edx-platform/manage.py lms syncdb --settings=aws
```

#调试
安装[httpie](https://github.com/jkbrzt/httpie)



###获取access token
[enable Open edX REST APIs](http://blog.just4fun.site/edx-api.html),只要进入/admin,取得有效access token即可

### 设置session 和 csrf
http post /siteapi/session  "AUTHORIZATION: Bearer xxx" sessionid_lms=xxx =xxx csrftoken_lms=xxx sessionid_cms=xxx csrftoken_cms=xxx

sessionid_lms
sessionid_lms

### create course （创建课程）
*  http post /siteapi/course  "AUTHORIZATION: Bearer xxx" org=json_org number=json_number run=json_run course_name=json_display_name username=wwj

### 为课程添加老师

http post /siteapi/teacher course_id=course-v1:edX+DemoX+Demo_Course username="staff" "AUTHORIZATION: Bearer 687f0d89069886911a4b08e7aae0c34ad5199b73"

### contral tab （调整课程默认标签）
*  http  post /siteapi/tab   tab_list=courseware+info+forum course_id=course-v1:edX+DemoX+Demo_Course username=staff  "AUTHORIZATION: Bearer xxx"

### enrollment(批量选课（课程创建时）)
ps:需要lms session

http post /siteapi/enrollment course_id=course-v1:edX+DemoX+Demo_Course username_list="staff,201011" "AUTHORIZATION: Bearer 687f0d89069886911a4b08e7aae0c34ad5199b73"te /siteapi/enrollment course_id=course-v1:edX+DemoX+Demo_Course username=staff "Authorization: Bearer xxx"


# 问题提醒
Open edX系统关机之后cookie失效，接口依赖于cookie，所以重启机器之后需要重新相关做配置

### todo
使用接口允许外置。

# 调试请求参数
使用`http://httpbin.org/`,原因返回你发送的http请求

*  http post http://httpbin.org/post tab_list=courseware+info+forum "Authorization: Bearer xxx"





#相似项目
*  [pmitros/edx-rest](https://github.com/pmitros/edx-rest/blob/master/src/edxrest.py)
*  [edx_manager_rest](https://github.com/wwj718/edx_manager_rest)
