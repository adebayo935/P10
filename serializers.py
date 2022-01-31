from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django import forms

class RegisterSerializer(ModelSerializer):

    def create(self, validated_data):
        data = validated_data
        new_user = User.objects.create(**data)
        new_user.set_password(data['password'])
        new_user.save()
        return new_user

    class Meta:
        model = User 
        fields = ["id","username", "first_name", "last_name",
                "email", "password",]


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password']


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id','user','project','permission','role']


class ContributorListSerializer(ModelSerializer):

    def get_user(self,instance):

        queryset_user = User.objects.filter(id=instance.user.id)
        serializer = UserListSerializer(queryset)
    
        return serializer.data

    class Meta:
        model = Contributor
        fields = ['user']



class ProjectDetailSerializer(ModelSerializer):

    contrib_user = SerializerMethodField()
    project_author = SerializerMethodField()
    issue_project = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id','title','description','type','author_user','project_author','contrib_user','issue_project']

    def create(self,validated_data):

        data = validated_data
        new_project = Project.objects.create(**data)
        new_project.save()
        return new_project

    def get_project_author(self,instance):

        user = User.objects.filter(id=instance.author_user.id)
        serializer = UserDetailSerializer(user[0])
    
        return serializer.data

    def get_contrib_user(self,instance):

        contrib = Contributor.objects.filter(project=instance)
        serializer = ContributorDetailSerializer(contrib, many=True)
    
        return serializer.data

    def get_issue_project(self,instance):

        issue = Issue.objects.filter(project=instance)
        serializer = IssueDetailSerializer(issue, many=True)
    
        return serializer.data



class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id','title','desc','tag','priority','project','status','author_user','assignee_user','created_time','comments']

    def get_comments(self,instance):

        comments = Comment.objects.filter(issue=instance)
        serializer = CommentDetailSerializer(comments, many=True)
    
        return serializer.data


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id','description','author_user','issue','created_time']
