# 引入path
from django.urls import path
from django.conf.urls import url
from . import views
# 正在部署的应用的名称
app_name = 'course'


urlpatterns = [
    path('submitproblem/',views.submitproblem),
    path('requsetproblem/<int:pk>/', views.requsetproblem),
    path('requestExerciseRecord/<int:pk>/',views.requestExerciseRecord),
    path('requestNext/',views.requestNext),
    path('startExercise/',views.startExercise)
]