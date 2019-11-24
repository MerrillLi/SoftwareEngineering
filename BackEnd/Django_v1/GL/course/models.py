from django.db import models
from datetime import datetime
from user.models import user_profile_stu

# Create your models here.
class CourseList(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"课程名字", default="")
    def __str__(self):
        return self.name

class Isvertify(models.Model):
    statu = models.CharField(max_length=100, verbose_name=u"审核状态", default="")

    def __str__(self):
        return self.statu

class Question(models.Model):
    course = models.ForeignKey(CourseList, verbose_name=u"所属课程",on_delete=models.CASCADE)
    content = models.TextField(verbose_name=u"题目内容", default='')
    answer = models.TextField(verbose_name=u"正确答案")
    choice_a = models.TextField(verbose_name=u"A选项", default="A.")
    choice_b = models.TextField(verbose_name=u"B选项", default="B.")
    choice_c = models.TextField(verbose_name=u"C选项", default="C.")
    choice_d = models.TextField(verbose_name=u"D选项", default="D.")
    note = models.TextField(verbose_name=u"备注信息", default= u"答案选XXX,因为XXX")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    count = models.IntegerField(verbose_name = u'提交人次', default='')
    evaluate_score=models.FloatField(verbose_name=u"题目得分", default='')
    true_rate=models.FloatField(verbose_name=u"题目正确率", default='')
    submit_user=models.ForeignKey(user_profile_stu, verbose_name=u"提交用户",on_delete=models.CASCADE)
    states =models.ForeignKey(Isvertify, verbose_name=u"审核状态",on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('-add_time',)

class Exersice(models.Model):
    student = models.ForeignKey(user_profile_stu, verbose_name = u"所属学生", on_delete=models.CASCADE)
    e_time = models.DateField(default=datetime.now,verbose_name=u"生成时间" )

    class Meta:
        ordering = ('-e_time',)
    
    def __str__(self):
        return self.student.name

class Item(Question):
    user_choice = models.CharField(max_length = 1, verbose_name=u"用户选择", default="" )
    exersice = models.ForeignKey(Exersice,verbose_name = u'练习场次', default = '',on_delete=models.CASCADE )
    ie_time = models.DateField(default=datetime.now, verbose_name=u"做题时间")
    class Meta:
        ordering = ('-ie_time',)
    

