from django.db import models
from datetime import datetime
from user_login.models import User

# Create your models here.
class CourseList(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"课程名字", default="")

class Isvertify(models.Model):
    statu = models.CharField(max_length=100, verbose_name=u"审核状态", default="")

class Question(models.Model):
    course = models.ForeignKey(CourseList, verbose_name=u"所属课程",on_delete=models.CASCADE)
    content = models.TextField(verbose_name=u"题目内容")
    answer = models.TextField(verbose_name=u"正确答案")
    choice_a = models.TextField(verbose_name=u"A选项", default="A.")
    choice_b = models.TextField(verbose_name=u"B选项", default="B.")
    choice_c = models.TextField(verbose_name=u"C选项", default="C.")
    choice_d = models.TextField(verbose_name=u"D选项", default="D.")
    note = models.TextField(verbose_name=u"备注信息", default= u"答案选XXX,因为XXX")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    evaluate_score=models.IntegerField(verbose_name=u"题目得分")
    true_rate=models.IntegerField(verbose_name=u"题目正确率")
    submit_user=models.ForeignKey(User, verbose_name=u"提交用户",on_delete=models.CASCADE)
    states =models.ForeignKey(Isvertify, verbose_name=u"审核状态",on_delete=models.CASCADE)

    class Meta:
        ordering = ('-add_time',)