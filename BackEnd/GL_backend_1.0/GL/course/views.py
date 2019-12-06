from django.shortcuts import render
from  .models import Question
# 导入 HttpResponse 模块
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
# 视图函数
from user.models import user_profile_stu, imageprofile,user_profile_teh
from .models import CourseList, Question, Exersice, Item,Papers,test_Item
import simplejson
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import check_password,make_password
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
import json
import random

def processTime(time):
    time=time.split('T')
    time0=time[0]
    print(time0)
    time1=time[1]
    time2=time1.split('.')
    time2=time2[0]
    time=time0+' '+time2
    return time


#上传试题
@csrf_exempt
def submitproblem(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        req = req["data"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)
        req["course_id"] = 1
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
def RequestProblem(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        req = req["data"]
        pk = req["pk"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key

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
                    #当请求全部题目时，只返回题干前20个字母
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
def requestExerciseRecord(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        req = req["data"]
        pk = req["pk"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key
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
        req = req["data"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key
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
        id=random.randint(1,6) #生成随机ID 
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
        print(response)
        return JsonResponse(response) 

#开始练习
#
#在数据库中创建一个新的练习记录
@csrf_exempt
def startExercise(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        #req=simplejson.loads(request.body)
        #req = req["data"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key
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
        req = req["data"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key
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
            
            #更新用户做题记录
            his = json.loads(user.ans_history)
            if len(his) >= 10:
                his.pop(list(his.keys())[0])
            his[question.id] = int(user_answer == question.answer)
            user.ans_history = json.dumps(his)
            user.save()

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
            response["answer"]=item.answer
            response["state"]=flag
        except Exception as e:
            response["msg"]=e
            print(e)
            return JsonResponse(response)
        return JsonResponse(response) 


@csrf_exempt      
def requestFirstPro(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        req = req["data"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)
        '''
        推荐第一道题
        '''
        print(recordlist)
        id=random.randint(1,6) #生成随机ID 
        try:
            ## 了解get 和 filter 的区别 
            question=Question.objects.get(id=id)              
            question.__dict__.pop("_state")
            #答案和注释不应该给用户看到
            question.__dict__.pop("answer")
            question.__dict__.pop("note")
            response["data"]= question.__dict__
            #count在提交答案的时候就更新了，这里人数-1
        except Exception as e:
            response["msg"]=e
            print(e)
            return JsonResponse(response)
        print(response)
        return JsonResponse(response) 



'''
获得所教的所有课程ID，以及名字，方便后面选课出题目
'''
@csrf_exempt
def getTeachCourse(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        req = req["data"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)
        user_tech=user_profile_teh.objects.get(user=user)

        courses = list(CourseList.objects.filter(teacher=user_tech))
        try:
            L = []
            for course in courses:
                course.__dict__.pop("_state")
                course_plus=course.__dict__
                course_plus['id']=course.id
                #当请求全部题目时，只返回前20个
                L.append(course_plus)
            response["data"]=L
        except Exception as e:
            response["msg"]=e
            print(e)
            return JsonResponse(response)
        return JsonResponse(response)



'''
根据课程ID去查询某个课程的所有题目
后期要考虑只加审核通过状态的题目
'''
@csrf_exempt
def getOneCoursePro(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        req = req["data"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        ID=req['courseID']
        user=User.objects.get(username=username)

        course=CourseList.objects.get(id=ID)
        questions = list(Question.objects.filter(course=course))
        try:
            L = []
            for question in questions:
                question.__dict__.pop("_state")
                L.append(question.__dict__)
            response["data"]=L
        except Exception as e:
            response["msg"]=e
            print(e)
            return JsonResponse(response)
        return JsonResponse(response)


#老师出卷
#1、数据库中创建一个paper项
#2、将输入字典的proID，全部生成test_Item
#3、关联test_Item和Paper
#同时更新数据库中的记录
@csrf_exempt
def creatPaper(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        req = req["data"]
        sessionid=request.session.session_key
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)
        pro_dictionary=list(req['proID'])
        date = req["date"]
        start=req['start']
        start=processTime(start)
        end=req['end']
        end=processTime(end)
        place=req['place']
        note=req['note']
        CourseID=req['CourseID']
        course=CourseList.objects.get(id=CourseID)
        ## 创建paper项
        paper = Papers(owner = user,course=course,start=start,end=end,place=place, note = note)
        paper.save()
        response['paperID']=paper.id
        
        ## 生成test_Item 关联paper项
        for proid in pro_dictionary:
            question=Question.objects.get(id=proid)
            test_item=test_Item(papers=paper,submit_user = question.submit_user,course=question.course,content=question.content,answer=question.answer,choice_a=question.choice_a, choice_b = question.choice_b, choice_c = question.choice_c, choice_d = question.choice_d, note = question.note)
            test_item.save()
        return JsonResponse(response) 

'''
获得试卷，传入课程名字
'''

@csrf_exempt
def getPaper(request):
    ##用户验证机制
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        req = req["data"]
        #sessionid=req["sessionid"]
        sessionid=request.session.session_key
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        user=User.objects.get(username=username)
        courseName=req["courseName"]
        course=CourseList.objects.get(name=courseName)
        papers=list(Papers.objects.filter(course=course))
        L=[]
        for paper in papers:
            paper.__dict__.pop("_state")
            L.append(paper.__dict__)
            test_items=list(test_Item.objects.filter(papers=paper))
            for test_item in test_items:
                test_item.__dict__.pop("_state")
                L.append(paper.__dict__)
        response["data"]=L
        return JsonResponse(response)


