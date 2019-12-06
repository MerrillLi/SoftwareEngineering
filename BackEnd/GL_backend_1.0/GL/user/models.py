from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import json

#用户
class user_profile_stu(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_profile_stu',primary_key=True)
    male_choices = (
        ('M', '男'),
        ('F', '女')
    )
    user_identity = (
        ('1', '学生'),
        ('2', '老师'),
    )
    identity=models.CharField("用户身份",max_length=128,choices=user_identity,default='1')
    phonenumber=models.CharField('电话号码', max_length=128,null=True,blank=True)
    name=models.CharField('姓名', max_length=128,null=True,blank=True)
    gender = models.CharField('性别', max_length=128,choices=male_choices,null=True,blank=True)
    age = models.CharField("年龄", max_length=128,null=True,blank=True)
    major = models.CharField("专业", max_length=128,null=True,blank=True)
    email = models.EmailField("邮件",max_length=128,null=True,blank=True)
    birth_data=models.DateField("出生日期",null=True,blank=True)
    institution=models.CharField("学院",max_length=128,null=True,blank=True,default = "工学院")
    capability=models.FloatField(verbose_name=u"能力值",default=0.6)
    ans_history = models.TextField(verbose_name=u"做题历史", default=json.dumps({'0':-1, '1':-1}))

    class Meta:
        verbose_name = '学生个人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.user)

    def get_absolute_url(self):
        return reverse('get_profile_stu', args=[self.user.id])


class user_profile_teh(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_profile_teh',primary_key=True)
    male_choices = (
        ('M', '男'),
        ('F', '女')
    )
    user_identity = (
        ('1', '学生'),
        ('2', '老师'),
    )
    identity=models.CharField("用户身份",max_length=128,choices=user_identity,default='1')
    phonenumber=models.CharField('电话号码', max_length=128,null=True,blank=True)
    name=models.CharField('姓名', max_length=128,null=True,blank=True)
    gender = models.CharField('性别', max_length=128,choices=male_choices,null=True,blank=True)
    major = models.CharField("专业", max_length=128,null=True,blank=True)
    email = models.EmailField("邮件",max_length=128,null=True,blank=True)
    institution=models.CharField("学院",max_length=128,null=True,blank=True,default = "工学院")

    class Meta:
        verbose_name = '老师个人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.user)

    def get_absolute_url(self):
        return reverse('get_profile_teh', args=[self.user.id])


#头像类
class imageprofile(models.Model):
    user = models.ForeignKey(User, verbose_name="用户头像", on_delete=models.CASCADE, related_name="user_imageprofile",null=True, blank=True)
    imgurl=models.CharField("头像路径",max_length=1000,null=True,blank=True, default = "gl")
    class Meta:
        verbose_name = '头像'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.user)

    def get_absolute_url(self):
        return reverse('头像', args=[self.user.id])

#验证用户类
class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
