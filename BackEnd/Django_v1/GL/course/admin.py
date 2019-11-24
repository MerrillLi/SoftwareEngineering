from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.CourseList)
admin.site.register(models.Isvertify)
admin.site.register(models.Question)
admin.site.register(models.Item)
admin.site.register(models.Exersice)
