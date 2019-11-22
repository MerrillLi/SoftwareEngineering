from django.shortcuts import render

# 导入 HttpResponse 模块
from django.http import HttpResponse

# 视图函数
def course(request):
    return HttpResponse("Hello World!")
