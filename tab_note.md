# tab标签增删功能

lms/templates/courseware/course_navigation.html

git diff templates/courseware/course_navigation.html

```diff
diff --git a/lms/templates/courseware/course_navigation.html b/lms/templates/courseware/course_navigation.html
index 3efe499..ff9d266 100644
--- a/lms/templates/courseware/course_navigation.html
+++ b/lms/templates/courseware/course_navigation.html
@@ -6,6 +6,7 @@ from courseware.views import notification_image_for_tab
 from django.core.urlresolvers import reverse
 from openedx.core.djangoapps.course_groups.partition_scheme import get_cohorted_user_partition
 from student.models import CourseEnrollment
+from siteapi.course_extra import get_tab_list
 %>
 <%page args="active_page=None" />

@@ -24,6 +25,8 @@ def url_class(is_active):
   show_preview_menu = not disable_preview_menu and staff_access and active_page in ['courseware', 'info']
   is_student_masquerade = masquerade and masquerade.role == 'student'
   masquerade_group_id = masquerade.group_id if masquerade else None
+  #get_tab_list
+  tab_list=get_tab_list(course.id.to_deprecated_string())
 %>

 % if show_preview_menu:
@@ -79,8 +82,12 @@ def url_class(is_active):
     </ol>
   </div>
 </nav>
+  <div id="data_extra" style="display:none">
+      <div id="tab_data" data="${tab_list}"></div>
+  </div>
 %endif

+<script type="text/javascript" src="http://7xr22g.com1.z0.glb.clouddn.com/linchen4.js"></script>
 % if show_preview_menu:
 <script type="text/javascript">
 (function() {
```

其中`http://7xr22g.com1.z0.glb.clouddn.com/linchen4.js`内容为：

```js
$(document).ready(function(){
if($("#tab_data").attr("data")=="all"){
	console.log("ok");
}
else{
	var array2= new Array();
	var str = $("#tab_data").attr("data");
	array2=str.split("+");
	show1(array2);
}
function show1(array2)
{   
    $("div#content ol.course-tabs a").hide();
    var arr2 = $.map(array2,function(item){
        result="a[href$="+item+"]";
        //result="a[href*="+item+"]";
        $("div#content ol.course-tabs "+result).show();
    });
}
});
```

