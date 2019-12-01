from django.db import models
from datetime import datetime
from user.models import user_profile_stu, user_profile_teh
from django.contrib.auth.models import User

# Create your models here.
class CourseList(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"课程名字", default="")
    user = models.ManyToManyField(user_profile_stu, verbose_name=u"选课学生") 
    teacher = models.ForeignKey(user_profile_teh, verbose_name=u"上课老师", on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Question(models.Model):

    course = models.ForeignKey(CourseList, verbose_name=u"所属课程",on_delete=models.CASCADE)
    content = models.TextField(verbose_name=u"题目内容", default='')
    answer = models.TextField(verbose_name=u"正确答案")
    

    choice_a = models.TextField(verbose_name=u"A选项", default="A.")
    choice_b = models.TextField(verbose_name=u"B选项", default="B.")
    choice_c = models.TextField(verbose_name=u"C选项", default="C.")
    choice_d = models.TextField(verbose_name=u"D选项", default="D.")


    note = models.TextField(verbose_name=u"备注信息", default= u"答案选XXX,因为XXX")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    
    count = models.IntegerField(verbose_name = u'提交人次', default=0)
    evaluate_score=models.FloatField(verbose_name=u"题目得分", default=0)
    true_rate=models.FloatField(verbose_name=u"题目正确率", default=0)
    submit_user=models.ForeignKey(User, verbose_name=u"提交用户",on_delete=models.CASCADE)
    states =models.CharField(verbose_name=u"审核状态", default = '未通过', max_length = 128)

    def __str__(self):
        return str(self.id)+":"+self.content

    class Meta:
        ordering = ('-add_time',)

class Exersice(models.Model):
    student = models.ForeignKey(User, verbose_name = u"所属学生", on_delete=models.CASCADE)
    e_time = models.DateTimeField(default=datetime.now,verbose_name=u"生成时间" )

    class Meta:
        ordering = ('-e_time',)
    
    def __str__(self):
        return str(self.id)+":"+str(self.e_time)

class Item(Question):
    user_choice = models.CharField(max_length = 1, verbose_name=u"用户选择", default="" )
    exersice = models.ForeignKey(Exersice,verbose_name = u'练习场次', default = '',on_delete=models.CASCADE )
    ie_time = models.DateTimeField(default=datetime.now, verbose_name=u"做题时间")

    class Meta:
        ordering = ('-ie_time',)

    def __str__(self):
        return str(self.id)+':'+self.content


class Papers(models.Model):
    student = models.ForeignKey(user_profile_stu, verbose_name = u"所属学生",on_delete=models.CASCADE)  # 一场考试 每个学生都有一张表
    e_time = models.DateTimeField(default=datetime.now,verbose_name=u"生成时间" )
    course = models.ForeignKey(CourseList,verbose_name = u"所属科目", on_delete=models.CASCADE )
    start = models.DateTimeField(default=datetime.now, verbose_name=u"开始时间")
    end = models.DateTimeField(default=datetime.now, verbose_name=u"结束时间")
    place = models.CharField(max_length = 128, verbose_name=u"考试地点", default="" )
    note = models.CharField(max_length = 128, verbose_name=u"考试类型", default="" )

    class Meta:
        ordering = ('-e_time',)
    
    def __str__(self):
        return str(self.course.name)+":"+str(self.id)

class test_Item(Question):
    user_choice = models.CharField(max_length = 1, verbose_name=u"用户选择", default="" )
    papers = models.ForeignKey(Papers,verbose_name = u'考试场次', default = '',on_delete=models.CASCADE )
    ie_time = models.DateTimeField(default=datetime.now, verbose_name=u"做题时间")

    class Meta:
        ordering = ('-ie_time',)

    def __str__(self):
        return str(self.id)+':'+self.content
    


# 注意：
# 数据库已经验证
# 我们没有实现在线考试功能，只实现了用户模拟测试的功能，所以每个用户有自己的试卷
# 一个用户一场考试就会有一张papers 对应的会有若干个test_item 用来保存用户的做题记录
# 老师查询题目，从question 中查找，将其所属课程的题目全部返回，返回前排个序按照分值高低（evaluate_score）返回