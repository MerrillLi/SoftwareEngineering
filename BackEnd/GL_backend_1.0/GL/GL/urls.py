from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import include
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView

urlpatterns = [
    #管理
    path('api/admin/', admin.site.urls),
    #跳转到关于用户的urls去
    path('api/user/',include('user.urls')),
    #跳转到关于course的urls去
    path('api/course/',include('course.urls')),

    #跳转到登陆界面
    path('',RedirectView.as_view(url="/index/")),

    #登陆界面
    path('index/log_in/',TemplateView.as_view(template_name="index.html")),
    #邮箱激活界面
    re_path('index/verify/(?P<verificationcode>[a-zA-Z0-9]{4})/',TemplateView.as_view(template_name="verify.html")),
    #验证是否成界面
    re_path('indexs/active/(?P<verificationcode>[a-zA-Z0-9]{4})/',TemplateView.as_view(template_name="active.html")),

]