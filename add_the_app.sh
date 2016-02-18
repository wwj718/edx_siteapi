#!/bin/bash

###########使用
#chomd + ./add_the_app.sh
#sudo ./add_the_app.sh

#往/edx/app/edxapp/edx-platform/lms/urls.py 结尾处添加
cat >> /edx/app/edxapp/edx-platform/lms/urls.py << EOF
####add by wwj
urlpatterns += (
url(r'siteapi/', include('siteapi.urls')),
)
EOF


#往/edx/app/edxapp/edx-platform/lms/env/aws.py 结尾处添加
cat >> /edx/app/edxapp/edx-platform/lms/envs/aws.py << EOF
####add by wwj
INSTALLED_APPS += ("siteapi",)
EOF


sudo /edx/bin/supervisorctl restart edxapp:
