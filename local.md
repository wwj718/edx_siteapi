# test
token: 687f0d89069886911a4b08e7aae0c34ad5199b73
ip: http://119.254.98.58:19880/

# 服务器
sudo -u www-data /edx/bin/python.edxapp /edx/app/edxapp/edx-platform/manage.py lms runserver 0.0.0.0:5000 --settings devstack

## access
*  http  http://119.254.98.58:19880/siteapi/access  "AUTHORIZATION: Bearer  687f0d89069886911a4b08e7aae0c34ad5199b73" 

## create course
###策略
*  采用编程的方法
    *  就可以只用一套cookie


http post http://119.254.98.58:5000/siteapi/course org=json_org number=json_number run=json_run course_name=json_display_name username="staff" "AUTHORIZATION: Bearer  687f0d89069886911a4b08e7aae0c34ad5199b73"
