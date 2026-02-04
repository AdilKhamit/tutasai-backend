from django.contrib import admin

from core import models

admin.site.register(models.User)
admin.site.register(models.Qualification)
admin.site.register(models.Contract)
admin.site.register(models.Object)
admin.site.register(models.AccessLetter)
admin.site.register(models.WorkCard)
admin.site.register(models.Protocol)
admin.site.register(models.AIAnalysis)
admin.site.register(models.ExpertConclusion)
