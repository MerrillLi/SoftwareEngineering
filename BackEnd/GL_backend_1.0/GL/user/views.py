from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse,HttpResponse
from .models import user_profile_stu, imageprofile, ConfirmString, user_profile_teh
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token ,rotate_token
from django.core.mail import send_mail,send_mass_mail,EmailMultiAlternatives
from django.views.decorators.http import require_http_methods
import simplejson
import json 
from django.conf import settings
import uuid
import hashlib
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import check_password,make_password
import random
import datetime
from django.core.mail import EmailMultiAlternatives
import hashlib
from django.utils import timezone

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if(type(user) == "QuerySet"):
        code = hash_code(user[0].username, now)
    else:
        code = hash_code(user.username, now)
    return code

#注册用户
@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    response = {} #字典
    if(request.method=="POST"):
        response["msg"] = 'true'
        req=simplejson.loads(request.body)
        req = req["data"]
        print(req)
        username=req["username"]
        password=req["password"]
        email=req["email"]
        identity=req["identity"]
        user=User.objects.filter(username=username)
        emailexist=User.objects.filter(email=email)
        #用户名/邮箱已存在
        print(user)
        if user:
            response["msg"]='f_ualready'
            print("OK")
            return JsonResponse(response)

        
        #如果不存在,创建一个user
        if len(user) == 0:
            user=User.objects.create_user(username=username,password=password)
            user.email=email
            user.is_active=True
            user.save()
            # 保存到数据库
            # 设置用户的身份

            if str(identity) == "student":
                profile=user_profile_stu(user=user)
                profile.identity=identity
                profile.save()
                

            if str(identity) =="teacher":
                profile = user_profile_teh(user=user)
                profile.identity = identity
                profile.save()
            
            img=imageprofile(user=user,imgurl=None)
            img.save()

        #如果用户已存在但是不是有效的,那么直接对这个用户发送邮件
        #发送邮件
        code = make_confirm_string(user)
        url = "http://172.16.143.9:8000/api/user/verify/"+ "?code={}".format(code) + "/"
        subject="激活邮件"
        content="点击下方进行激活"
        recipient_emial=[email]
        html_content="<p>欢迎使用,请点击</p><a href='"+url+"'>此处</a><p>进行验证<p>"
        from_email=settings.DEFAULT_FROM_EMAIL
        mail=EmailMultiAlternatives(subject,content,from_email,recipient_emial)
        mail.attach_alternative(html_content,"text/html")
        try:
            mail.send()
            #发送成功，把验证码保存在数据库中
            ConfirmString.objects.create(code=code, user=user,)
        except Exception as e:
            response["msg"]="f_send" #发送失败
            return JsonResponse(response)
        response["msg"] = 'S_toemail'
        return JsonResponse(response)


def user_confirm(request):
    response = {}
    code = request.GET.get('code', None)
    code = code.strip('/')
    print(code)
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        response["msg"] = 'code_fault'
        return JsonResponse(response)

    c_time = confirm.c_time
    #now = datetime.datetime.now()
    now = timezone.now()
    
    if now > (c_time + datetime.timedelta(settings.CONFIRM_DAYS)).replace():
        confirm.user.delete()
        response["msg"] = 'code_expire'
        return JsonResponse(response)
    else:
        confirm.user.is_active = True
        confirm.user.save()
        confirm.delete()
        response["msg"] = 'success'
        return JsonResponse(response)

#找回密码
@csrf_exempt
@require_http_methods(["POST"])
def findpas(request):
    response={}
    if(request.method=="POST"):
        response["msg"]="true"
        req=simplejson.loads(request.body)
        req = req["data"]
        email=req["email"]
        user = User.objects.filter(email=email)
        if(type(user) == "QuerySet"):
            user = user[0]
        if user:
            # 生成随机字符串
            code = make_confirm_string(user)
            url = "http://172.16.143.9:8000/user/verifyandsetpas/"+ "?code={}".format(code) + "/"
            subject = "找回密码"
            content = "这是您的验证码："+code+"\n如果您不是当前用户，请忽略"
            html_content="<p>欢迎使用,请点击</p><a href='"+url+"'>此处</a><p>进行验证<p>"
            recipient_emial = [email]
            from_email = settings.DEFAULT_FROM_EMAIL
            mail = EmailMultiAlternatives(subject, content, from_email, recipient_emial)
            try:
                mail.send()
                #发送成功，把验证码保存在数据库中
                ConfirmString.objects.create(code=code, user=user,)
            except Exception as e:
                response["msg"] = "f_send"  # 发送失败
        else:
            response["msg"]="false"
        return JsonResponse(response)

#验证并重置密码
@csrf_exempt
@require_http_methods(["POST"])
def verifyandsetpas(request):
    response={}
    req=simplejson.loads(request.body)
    req = req["data"]
    password=req["password"]
    code = request.GET.get('code', None)
    code = code.strip('/')
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        response["msg"] = 'code_fault'
        return JsonResponse(response)

    c_time = confirm.c_time
    now = datetime.datetime.now()

    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        response["msg"] = 'code_expire'
        return JsonResponse(response)
    else:
        response["msg"] = 'fail'
        confirm.user.password=req["newpassword"]
        confirm.user.save()
        confirm.delete()
        response["msg"] = 'success'
    return JsonResponse(response)

#修改密码
@csrf_exempt
@require_http_methods(["POST"])
def changepas(request):
    response = {}
    if request.method == 'POST':
        response["msg"] = "ture"
        req = simplejson.loads(request.body)
        req = req["data"]
        username = req['username']
        oldpassword=req["oldpassword"]
        newpassword=req["newpassword"]
        try:
            user = User.objects.get(username=username)
            if check_password(oldpassword,user.password):
                user.password=newpassword
                user.save()
            else:
                response["msg"]="false"
        except Exception as e:
            response["msg"]="false"
        return JsonResponse(response)

@csrf_exempt
#登陆
def log_in(request):
    # 设置响应
    response={}
    if request.method=="POST":
        # str=request.META.get("HTTP_SESSIONID")
        msg = 'true'
        req = json.loads(request.body.decode())
        req = req['data']
        username=req['username']
        password=req['password']
        print("req:", req)
        #identity = req['identity']
        try:
            user = User.objects.get(username=username)  # 这个设置是为了更详细的检查出错误来,因为这个地方get函数不会返回none，一旦找不到，便会给一个exception
            user = authenticate(username=username, password=password)  # 而authenticate就能返回一个none
            print(user)
            if user:
                login(request,user)
                request.session['is_login']=True
                request.session['username']=username
                cache.set(request.session.session_key,{"username":username,"is_login":True})
                print("DENGLU:", request.session.session_key)
            else:
                msg = "密码错误"
            
            userstuprofile = list(user_profile_stu.objects.filter(user=user))
            if(len(userstuprofile) == 0):
                userstuprofile=list(user_profile_teh.objects.filter(user=user))
            print(userstuprofile)
            if len(userstuprofile)>0:
                response["identity"]=userstuprofile[0].identity
            else:
                response["identity"]=userstuprofile.identity
            
            response["msg"]=msg
            print("sessionid:" , request.session.session_key)
            response["sessionid"]=request.session.session_key
            return JsonResponse(response)
        except Exception as e:
            print(e)
            msg = "用户不存在"
            response["msg"]=msg
            return JsonResponse(response)
    get_token(request)  # 产生一个token 用于csrf验证
    return JsonResponse(response)

@csrf_exempt
#登出
def log_out(request):
    
    # del request.session["sessionid"]
    #删除cache中的配置
    logout(request)
    #cache.delete(request.session.session_key)
    response={"msg":"true"}
    return JsonResponse(response)

@csrf_exempt
#获取个人信息
def get_profile(request):
    req = simplejson.loads(request.body)
    req = req["data"]
    print(req)
    identity=req.get("identity",None)
    #sessionid = req.get("sessionid",None)
    #print(type(identity))
    sessionid=request.session.session_key
    print("QINGQIUGERENXINXI:", sessionid)
    dic=cache.get(sessionid)
    #sessionid 过期
    if dic is None:
        return JsonResponse({"msg":"expire"})
    username=cache.get(sessionid).get("username",None)
    is_login = cache.get(sessionid).get("is_login", False)  # 如果is_login没有设置值的话，默认为False
    response = {}
    msg = 'true'
    #登陆成功
    #print(is_login)
    print(username)
    if is_login:
        user=User.objects.get(username=username)

        try:
            userprofile = user_profile_stu.objects.filter(user=user)
            if(len(userprofile) == 0):
                userprofile = user_profile_teh.objects.filter(user=user)
            userprofile = userprofile[0]

            if (  str(userprofile[0].identity) == 'student'):
                response["phonenumber"]=userprofile.phonenumber
                response["name"] = userprofile.name
                response["gender"] = userprofile.gender
                response["age"]=userprofile.age
                response["major"] = userprofile.major
                response["email"]=userprofile.email
                response["birth_data"]=userprofile.birth_data
                response["user_id"] = user.id
                response["identity"]=userprofile.identity
                response["institution"]=userprofile.institution
                response["msg"]=msg
            else:
                response["phonenumber"]=userprofile.phonenumber
                response["name"] = userprofile.name
                response["gender"] = userprofile.gender
                response["age"]=userprofile.age
                response["major"] = userprofile.major
                response["email"]=userprofile.email
                response["user_id"] = user.id
                response["identity"]=userprofile.identity
                response["institution"]=userprofile.institution
                response["msg"]=msg

            '''
            # 头像获取
            img=imageprofile.objects.filter(user=user)[0]
            response["imgurl"] = img.imgurl
            '''
            print(response)
            return JsonResponse(response)
        except Exception as e:
            print(e)
            return JsonResponse(response)
    else:
        response["msg"]="is_login_false"
        return JsonResponse(response)

@csrf_exempt
#更新个人信息
def update_profile(request):
    response = {}
    if(request.method=="POST"):
        response["msg"] = "true"
        sessionid=request.session.session_key
        dic=cache.get(sessionid)
        req=simplejson.loads(request.body)
        req = req["data"]
        #cache过期
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        is_login=dic["is_login"]
        identity = req.get("identity", None)
        #获取用户
        #block=req.get("block",None)
        user = User.objects.get(username=username)
        if is_login:
            try:
                userprofile = user_profile_stu.objects.filter(user=user)
                if(len(userprofile) == 0):
                    userprofile = user_profile_teh.objects.filter(user=user)
                userprofile = userprofile[0]

                if(str(userprofile.identity) == 'student'):
                    userprofile.name = req["name"]
                    userprofile.gender = req["gender"]
                    '''
                    # 头像
                    image = imageprofile.objects.get(user=user)
                    image.imgurl = req["imgurl"]
                    image.save()
                    '''
                    userprofile.age = req["age"]
                    userprofile.birth_data = req["birth_data"]
                    userprofile.major = req["major"]
                    userprofile.email = req["email"]
                    userprofile.phonenumber = req["phonenumber"]
                    userprofile.save()
                    response["msg"]="true"
                else:
                    userprofile.name = req["name"]
                    userprofile.gender = req["gender",None]
                    userprofile.age = req["age"]
                    #userprofile.birth_data = req["birth_data"]
                    userprofile.major = req["major"]
                    userprofile.email = req["email"]
                    userprofile.phonenumber = req["phonenumber"]
                    userprofile.save()
                    response["msg"]="true"
            except Exception as e:
                response['msg']=e
                return JsonResponse(response)
    get_token(request)
    print(response)
    return JsonResponse(response)

