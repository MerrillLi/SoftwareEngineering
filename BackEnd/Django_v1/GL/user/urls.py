from django.urls import path
from . import views

urlpatterns=[
    #保证这个应用里面的都是接口，是给前端提供数据的接口

    #注册
    path('register/',views.register),
    #验证邮箱
    path('active/',views.active),
    #登陆
    path('login/',views.log_in),
    #登出
    path('logout/',views.log_out),
    #更改密码
    path('changepas/',views.changepas),
    #找回密码
    path('findpas/',views.findpas),
    #验证并重置密码
    path('verifyandsetpas/',views.verifyandsetpas),
    #获取个人信息
    path('get_profile/', views.get_profile, name='get_profile'),
    #更新个人信息
    path('update_profile/', views.update_profile, name='update_profile'),
    #函数验证的函数
    path('verify/',views.active,name='verify')


]
