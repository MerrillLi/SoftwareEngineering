from django.shortcuts import render
import Question
# 导入 HttpResponse 模块
from django.http import HttpResponse

# 视图函数
def course(request):
    return HttpResponse("Hello World!")

class SubmitProblemList(View):
    """提交题目列表"""

    def get(self, request):
        questions = Question.objects.filter(submit_user=request.user)
    return HttpResponse(questions)