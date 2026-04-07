from django.contrib import admin
from tasks.models import Task, TaskDetail, Project
from users.models import UserProfile

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskDetail)
admin.site.register(Project)
admin.site.register(UserProfile)