
from django.conf.urls import url, include
from rest_framework import routers

from myapp import views


router = routers.DefaultRouter()
# 帮我们自动生成4个url
router.register(r'xxxx',views.View1View)
## 帮我们自动生成4个url
router.register(r'rt',views.View1View)



urlpatterns = [

 url(r'^(?P<version>[v1|v2]+)/',include(router.urls)),

 # url(r'^users/',views.UsersView.as_view()),
 url(r'^(?P<version>[v1|v2]+)/users/$',views.UsersView.as_view(),name='uuu'),
 url(r'^(?P<version>[v1|v2]+)/django/$',views.DjangoView.as_view(),name='django'),
 url(r'^(?P<version>[v1|v2]+)/parser/$',views.ParserView.as_view(),name='parser'),
 url(r'^(?P<version>[v1|v2]+)/roles/$',views.RolesView.as_view(),name='roles'),
 url(r'^(?P<version>[v1|v2]+)/userinfo/$',views.UserinfoView.as_view(),name='userinfo'),
 url(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$',views.GroupView.as_view(),name='gp'),
 url(r'^(?P<version>[v1|v2]+)/usergroup/$',views.UserGroupView.as_view(),name='usergroup'),
 url(r'^(?P<version>[v1|v2]+)/page1/$',views.Page1View.as_view()),
 # url(r'^(?P<version>[v1|v2]+)/view1/$',views.View1View.as_view()),


 # 执行了内部的对应关系，发送get请求的时候，执行对应的list方法，发送post请求的时候执行对应的xxx方法
# http://127.0.0.1:8000/myapp/v1/view1/?format=json  渲染器根据传的url不同，渲染不同
 url(r'^(?P<version>[v1|v2]+)/view1/$',views.View1View.as_view({'get':'list','post':'create'})),
# http://127.0.0.1:8000/myapp/v1/view1.json
 url(r'^(?P<version>[v1|v2]+)/view1\.(?P<format>\w+)$',views.View1View.as_view({'get':'list','post':'create'})),


 url(r'^(?P<version>[v1|v2]+)/view1/(?P<pk>\d+)$',views.View1View.as_view({'get':'retrieve','post':'create','delete':'destroy','put':'update','patch':'partial_update'})),
 url(r'^(?P<version>[v1|v2]+)/view1/(?P<pk>\d+)\.(?P<format>\w+)$',views.View1View.as_view({'get':'retrieve','post':'create','delete':'destroy','put':'update','patch':'partial_update'})),

 url(r'^(?P<version>[v1|v2]+)/test/$', views.TestView.as_view()),


]
