# 引入path
from django.urls import path
from django.conf.urls import url
from . import views
# 正在部署的应用的名称
app_name = 'course'

#审核题目功能未做

urlpatterns = [
    path('submitproblem/',views.submitproblem),
    path('RequestProblem/', views.RequestProblem),
    #path('requsetproblem/', views.requsetproblem),
    path('requestExerciseRecord/',views.requestExerciseRecord),
    path('requestNext/',views.requestNext),
    path('requestFirstPro/',views.requestFirstPro),# 请求第一道题目
    path('startExercise/',views.startExercise),
    path('submitAnswer/',views.submitAnswer),
    path('creatPaper/',views.slectQuestions),# 创建试卷
    path('getTeachCourse/',views.getTeachCourse),# 查询所教课程 
    path('getOneCoursePro/',views.getOneCoursePro), # 查询某门课程的所有题目
    path('getPaper/',views.getPaper)# 获得试卷
]
