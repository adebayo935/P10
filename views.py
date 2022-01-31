from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action
from .permissions import *
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

class SignUpView(ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    model = User


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):

        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    permission_classes = [IsProjectAuthorAuthenticated]
    serializer_class = ProjectDetailSerializer

    def get_queryset(self):

        queryset = Project.objects.all()

        id = self.request.GET.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
        return queryset


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorDetailSerializer
    permission_classes = [IsAuthorAuthenticated]

    def get_queryset(self, *args, **kwargs):

        queryset = Contributor.objects.all()
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A Project with this id does not exist')
        return queryset.filter(project=project)


class UserViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = UserDetailSerializer

    def get_queryset(self):

        queryset = User.objects.all()

        id = self.request.GET.get('id')
        if id is not None:
            queryset = queryset.filter(id=id)
        return queryset


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueDetailSerializer
    permission_classes = [IsContributorAuthenticated]

    def get_queryset(self, *args, **kwargs):
        
        queryset = Issue.objects.all()
        project_id = self.kwargs.get("project_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound('A Project with this id does not exist')
        return queryset.filter(project=project)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentDetailSerializer
    permission_classes = [IsCommentAuthorAuthenticated]

    def get_queryset(self, *args, **kwargs):

        queryset = Comment.objects.all()
        issue_id = self.kwargs.get("issue_pk")
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise NotFound('An Issue with this id does not exist')
        return queryset.filter(issue=issue)


