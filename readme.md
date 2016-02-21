#siteapi
将edx视为子系统，为外部提供RESTful风格的api

#设计
*  这部分代码组织形式为django app

#功能
*  站点级别的管理
*  用户管理（增删）
*  课程创建
*  成绩查询
*  注册课程
*  ...其他的等你一起来添加 :)


#调试
安装[httpie](https://github.com/jkbrzt/httpie)

###获取access token
[enable Open edX REST APIs](http://blog.just4fun.site/edx-api.html),只要进入/admin,取得有效access token即可

###开始调试
*  http get http://127.0.0.1:5000/siteapi/user 'Authorization: Bearer xxxxxxxxxxxxx' (xxxxxxxxx为你的access token )
*  http post http://127.0.0.1:5000/siteapi/user username=wwj password=wwj 'Authorization: Bearer xxxxxxxxxxxxx'

###create course
*  http  post http://127.0.0.1:5000/siteapi/course   org=json_org number=json_number run=json_run display_name=json_display_na
me  "AUTHORIZATION: Bearer  xxx"

###edit tab
*  http  delete http://127.0.0.1:5000/siteapi/tab tab_num=4   course_id=xxx  "AUTHORIZATION: Bearer xxx"
*  http  get http://127.0.0.1:5000/siteapi/tab   course_id=xxx  "AUTHORIZATION: Bearer xxx"
