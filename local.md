# test
token: 687f0d89069886911a4b08e7aae0c34ad5199b73
ip: http://119.254.98.58:19880/

# 服务器
sudo -u www-data /edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py lms runserver 0.0.0.0:5000 --settings devstack

http://119.254.98.58:5000

### 测试服务器
测试地址:http://119.254.98.58:19880/

取消不必要的服务

```
cd /edx/app/supervisor/conf.available.d
sudo ipython

for name in os.listdir("."):
		new_name=name.replace('.conf','.conf_bak')
		os.rename(name,new_name)
		
#开启lms/cms
sudo mv lms.conf_bak lms.conf
sudo mv cms.conf_bak cms.conf

```


## access
*  http  http://119.254.98.58:19880/siteapi/access  "AUTHORIZATION: Bearer  687f0d89069886911a4b08e7aae0c34ad5199b73" 

## create course

http post http://119.254.98.58:5000/siteapi/course org=json_org number=json_number run=json_run course_name=json_display_name username="staff" "AUTHORIZATION: Bearer  687f0d89069886911a4b08e7aae0c34ad5199b73"



### management (不需要写文档)
sudo -u www-data /edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py lms hello --settings devstack


参考：
*  [enrollment/management/commands/enroll_user_in_course.py](https://github.com/edx/edx-platform/blob/master/common/djangoapps/enrollment/management/commands/enroll_user_in_course.py)
*  [学生加入群组](https://github.com/edx/edx-platform/blob/master/common/djangoapps/student/management/commands/add_to_group.py)
*  [批量修改注册](https://github.com/edx/edx-platform/blob/master/common/djangoapps/student/management/commands/change_enrollment.py)
*  [创建用户](https://github.com/edx/edx-platform/blob/master/common/djangoapps/student/management/commands/create_user.py)
    *  https://github.com/edx/edx-platform/blob/aa078dfda2c07c6d5a0bde8f0bfd712ba9f33349/common/djangoapps/student/views.py#L1474 创建用户的钩子

*  以上的demo需要修改，课程代号滞后 :course-v1:edX+DemoX+Demo_Course
*  学习from optparse import make_option
*  这里边的函数都没有request


sudo -u www-data /edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py lms  create_user --username test123 --name test123  --password test123 --email test123@qq.com --settings devstack


### tab
http post http://119.254.98.58:5000/siteapi/tab tab_list=courseware+info+forum course_id=course-v1:edX+DemoX+Demo_Course  "AUTHORIZATION: Bearer 687f0d89069886911a4b08e7aae0c34ad5199b73"

### 添加老师

http post http://119.254.98.58:5000/siteapi/teacher course_id=course-v1:edX+DemoX+Demo_Course  username="staff" "AUTHORIZATION: Bearer  687f0d89069886911a4b08e7aae0c34ad5199b73"

### 批量选课（课程创建时）
需要lms session


http post http://119.254.98.58:5000/siteapi/enrollment course_id=course-v1:edX+DemoX+Demo_Course  username_list="staff,201011" "AUTHORIZATION: Bearer  687f0d89069886911a4b08e7aae0c34ad5199b73"

# 问题
 关机之后cookie失效,可能需要登录页面重新获取

