# 引入path
from django.urls import path
from .views import SubmitProblemList
# 正在部署的应用的名称
app_name = 'course'

urlpatterns = [
    path('course/', views.course, name='course'),
    url(r'^problemList/$', SubmitProblemList.as_view(), name="SubmitProblemList"),
]