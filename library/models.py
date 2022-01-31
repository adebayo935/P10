from django.db import models
from django.contrib.auth.models import (AbstractUser, PermissionsMixin)
from django.conf import settings
from .managers import UserManager


class User(AbstractUser):
    
    username = models.CharField(max_length=128,unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    author_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='project_author')

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='contrib_user')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contrib_project')
    permission = models.CharField(max_length=128)
    role = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=128)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issue_project')
    status = models.CharField(max_length=128)
    author_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='issue_author')
    assignee_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Comment(models.Model):
    description = models.CharField(max_length=128)
    author_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comment_author')
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
