from rest_framework.permissions import BasePermission
from .models import *
 
class IsProjectAuthorAuthenticated(BasePermission):
 
    def has_permission(self, request, view):
    
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):

        project = Project.objects.filter(id=obj.id)
        if project[0].author_user == request.user:
            return True
        else: 
            return False

class IsAuthorAuthenticated(BasePermission):
 
    def has_permission(self, request, view):

        project = Project.objects.filter(id=request.data['project'])
        if project[0].author_user == request.user:
            return True
        else: 
            return False

    def has_object_permission(self, request, view, obj):

        return True


class IsContributorAuthenticated(BasePermission):
 
    def has_permission(self, request, view):

        contributors = Contributor.objects.filter(project=request.data['project'])
        for contributor in contributors:
            if contributor.user == request.user:
                return True
            else:
                pass
        return False

    def has_object_permission(self, request, view, obj):
  
        issue = Issue.objects.filter(id=obj.id)
        if issue[0].author_user == request.user:
            return True
        else: 
            return False

class IsCommentAuthorAuthenticated(BasePermission):
 
    def has_permission(self, request, view):

        issue = Issue.objects.get(id=request.data['issue'])
        contributors = Contributor.objects.filter(project=issue.project)
        for contributor in contributors:
            if contributor.user == request.user:
                return True
            else:
                pass
        return False

    def has_object_permission(self, request, view, obj):

        comment = Comment.objects.get(id=obj.id)
        if comment.author_user == request.user:
            return True
        else:
            return False