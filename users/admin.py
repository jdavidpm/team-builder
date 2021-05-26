from django.contrib import admin
from .models import *

admin.site.register(Field)
admin.site.register(Language)
admin.site.register(Framework)
admin.site.register(Tool)
admin.site.register(Distribution)
admin.site.register(Profile)
admin.site.register(FeaturedWork)
admin.site.register(Career)
admin.site.register(Student)
admin.site.register(Academy)
admin.site.register(Subject)
admin.site.register(Project)

class MembersInlineAdmin(admin.TabularInline):
    model = Team.members.through

class TeamAdmin(admin.ModelAdmin):
    fields = ['founder', 'name', 'private', 'projects', 'average_eval']
    inlines = [MembersInlineAdmin, ]

admin.site.register(Team, TeamAdmin)
admin.site.register(Membership)
admin.site.register(TeamEvaluation)
admin.site.register(JoinRequest)
admin.site.register(JoinInvitation)
admin.site.register(ProjectActivity)
admin.site.register(Task)
admin.site.register(TaskActivity)
admin.site.register(Association)
