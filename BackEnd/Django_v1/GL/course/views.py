from django.shortcuts import render
from  .models import Question
# 导入 HttpResponse 模块
from django.http import HttpResponse
from django.views.generic.base import View
# 视图函数
def problem(request,year):

    return HttpResponse(year)

class SubmitProblemList(View):
    """提交题目列表"""

    def get(self, request):
        questions = Question.objects.filter(count=21)
        print(questions)
        return HttpResponse(questions)
        