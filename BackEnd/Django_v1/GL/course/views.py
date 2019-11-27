from django.shortcuts import render
from  .models import Question
# 导入 HttpResponse 模块
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
# 视图函数
from user.models import user_profile_stu, imageprofile
from .models import CourseList, Question, Exersice, Item
import simplejson
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import check_password,make_password
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User


#上传试题
@csrf_exempt
def submitproblem(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        sessionid=req["sessionid"]
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)
        to_which_course = CourseList.objects.get(id=req["course_id"])
        # 先数据库查询course_id, 没有则新建
        content=req["content"]
        answer=req["answer"]
        choice_a = req["choice_a"]
        choice_b = req["choice_b"]
        choice_c = req["choice_c"]
        choice_d = req["choice_d"]
        note = req["note"]
        
        try:
            print(user)
            question = Question(submit_user = user,course=to_which_course,content=content,answer=answer,choice_a=choice_a, choice_b = choice_b, choice_c = choice_c, choice_d = choice_d, note = note)
            question.save()
            response["msg"]="true"
            response["question_id"]=question.id
            response["question_time"]=question.add_time
        except Exception as e:
            response["msg"]=e
            print(e)
            return JsonResponse(response)
        return JsonResponse(response)


# 查询出题记录
# 通过userid查询其所有出过的题目
# （题目的id 也会返回）
# 如果pk 值不为-1 则只返回相应的题目
@csrf_exempt
def requsetproblem(request,pk):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        sessionid=req["sessionid"]
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)

        if (pk == 0):
            # userprofile = user_profile_stu.objects.get(user=user) # 用户个人信息
            questions = list(Question.objects.filter(submit_user=user))
            try:
                L = []
                for question in questions:
                    question.__dict__.pop("_state")
                    #当请求全部题目时，只返回前20个
                    if len(question.__dict__["content"]) >=20:
                        question.__dict__["content"]=question.__dict__["content"][0:20]
                    L.append(question.__dict__)
                response["data"]=L
            except Exception as e:
                response["msg"]=e
                print(e)
                return JsonResponse(response)
            return JsonResponse(response)
        else:
            try:
                ## bug 无法序列化
                ## 了解get 和 filter 的区别 
                question=Question.objects.get(id=pk)              
                question.__dict__.pop("_state")
                response["data"]= question.__dict__
            except Exception as e:
                response["msg"]=e
                print(e)
                return JsonResponse(response)
            return JsonResponse(response) 

#查看用户的练习场次
#pk值为0的时候，查看具体练习场次
#pk值为其他值的时候，查看练习记录数据库里ID为pk值的题目
@csrf_exempt
def requestExerciseRecord(request,pk):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        sessionid=req["sessionid"]
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)

        if (pk == 0):
            # userprofile = user_profile_stu.objects.get(user=user) # 用户个人信息
            exersices = list(Exersice.objects.filter(student=user))
            try:
                L = []
                for exersice in exersices:
                    exersice.__dict__.pop("_state")
                    #当请求全部题目时，只返回前20个
                    L.append(exersice.__dict__)
                response["data"]=L
            except Exception as e:
                response["msg"]=e
                print(e)
                return JsonResponse(response)
            return JsonResponse(response)
        else:
            try:
                ## 有问题，当session确认后，可以直接通过id查看别人的场次？是否安全。
                ## 了解get 和 filter 的区别 
                exercise=Item.objects.get(id=pk)        
                exercise.__dict__.pop("_state")
                response["data"]= exercise.__dict__
            except Exception as e:
                response["msg"]=e
                print(e)
                return JsonResponse(response)
            return JsonResponse(response)

#练习的时候，请求下一道试题
#提交对上一题的得分评价
#算法根据之前做的题目产生下一道题目
@csrf_exempt
def requestNext(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        sessionid=req["sessionid"]
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)
        recordlist=req['record']
        score=req['score']
        '''
        这里填写读取req里的字典
        要从审核状态为通过的里面找
        然后算法产生推荐题目ID
        '''
        print(recordlist)
        id=1 #测试的时候推荐7
        try:
            ## 了解get 和 filter 的区别 
            question=Question.objects.get(id=id)              
            question.__dict__.pop("_state")
            #答案和注释不应该给用户看到
            question.__dict__.pop("answer")
            question.__dict__.pop("note")
            response["data"]= question.__dict__
            #count在提交答案的时候就更新了，这里人数-1
            score=(question.evaluate_score*(question.count-1)+score)/(question.count+1)
            Question.objects.filter(id=id).update(evaluate_score=score)
        except Exception as e:
            response["msg"]=e
            print(e)
            return JsonResponse(response)
        return JsonResponse(response) 

#开始练习
#
#在数据库中创建一个新的练习记录
@csrf_exempt
def startExercise(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        sessionid=req["sessionid"]
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)

        try:
            print(user)
            exercise = Exersice(student = user)
            exercise.save()
            response["msg"]="true"
            response["turnID"]=exercise.id
            response["turnTime"]=exercise.e_time
        except Exception as e:
            response["msg"]=e
            print(e)
            return JsonResponse(response)
        return JsonResponse(response) 


#提交选项答案，返回正确答案
#1、返还正确答案，notes
#2、更新question表单中对于该数据的描述，做题人数，正确率等
#3、保存这次item记录到数据库
#同时更新数据库中的记录
@csrf_exempt
def submitAnswer(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        sessionid=req["sessionid"]
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)
        
        user_answer=req['answer']
        problemId=req['proID']
        turnID=req['turnID']
        try:
            print(user)
            exercise=Exersice.objects.get(id=turnID)
            question=Question.objects.get(id=problemId)
            flag="false"
            if user_answer==question.answer:
                true_rate=(question.true_rate*question.count+1)/(question.count+1)
                flag="true"
            else:
                true_rate=(question.true_rate*question.count+1)/(question.count+1)
            count=question.count+1
            #更新question里的描述
            Question.objects.filter(id=problemId).update(count=count,true_rate=true_rate)
            item = Item(exersice = exercise,user_choice = user_answer,submit_user = question.submit_user,course=question.course,content=question.content,answer=question.answer,choice_a=question.choice_a, choice_b = question.choice_b, choice_c = question.choice_c, choice_d = question.choice_d, note = question.note)
            item.save()
            response["msg"]="true"
            response["ItemID"]=item.id
            response["SubmitTime"]=item.ie_time
            response["state"]=flag
        except Exception as e:
            response["msg"]=e
            print(e)
            return JsonResponse(response)
        return JsonResponse(response) 
        







