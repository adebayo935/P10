from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'first_name', 'last_name','email','is_active','is_staff')
    list_filter = ('username', 'first_name', 'last_name','is_active','is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name','email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name','email', 'password','is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

class CustomIssueAdmin(admin.ModelAdmin):
    model = Issue
    list_display = ("id",'title', 'desc', 'priority','project','status','author_user','assignee_user','created_time')
    list_filter = ('id','title', 'desc', 'priority','project','status','author_user','assignee_user','created_time')


class CustomContributorAdmin(admin.ModelAdmin):
    model = Contributor
    list_display = ('id','user', 'project', 'permission','role')
    list_filter = ('id','user', 'project', 'permission','role')


class CustomProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('id','title', 'description', 'type','author_user')
    list_filter = ('id','title', 'description', 'type','author_user')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Issue, CustomIssueAdmin)
admin.site.register(Contributor, CustomContributorAdmin)
admin.site.register(Project, CustomProjectAdmin)