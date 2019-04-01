from django.contrib import admin
from .models import Class, Technology, Title, Request, SkillLevels, Message

# Register your models here.
admin.site.register(Class)
admin.site.register(Technology)
admin.site.register(Title)
admin.site.register(Request)
admin.site.register(SkillLevels)
admin.site.register(Message)