# 引入path
from django.urls import path
from django.conf.urls import url
from . import views
# 正在部署的应用的名称
app_name = 'course'


urlpatterns = [
    path('problem/<int:year>/', views.problem, name='problem'),

]