# 引入path
from django.urls import path
from . import views
# 正在部署的应用的名称
app_name = 'course'

urlpatterns = [
    path('course/', views.course, name='course'),
]