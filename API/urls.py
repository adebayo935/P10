from django.contrib import admin
from django.urls import path, include
#from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers


from library.views import *

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')
'''router.register('contributors', ContributorViewset, basename='contributors')
router.register('issues', IssueViewset, basename='issues')
router.register('comments', CommentViewset, basename='comments')'''
router.register('users', UserViewset, basename='users')
router.register('register', SignUpView, basename="signup")

'''router.register('admin/users', AdminUserViewset, basename='admin-users')
router.register('admin/projects', AdminProjectViewset, basename='admin-project')
router.register('admin/projects/<int:id>/contributors', AdminContributorViewset, basename='admin-contributors')
router.register('admin/projects/<int:id>/issues', AdminIssueViewset, basename='admin-issues')
router.register('admin/projects/<int:id>/issues/<int:id>/comments', AdminCommentViewset, basename='admin-comments')'''

domains_router = routers.NestedSimpleRouter(router,'projects', lookup="project")
domains_router.register('contributors',ContributorViewset, basename='project-contributors')
domains_router.register('issues', IssueViewset, basename='project-issues')

second_router = routers.NestedSimpleRouter(domains_router,'issues', lookup="issue")
second_router.register('comments', CommentViewset, basename='comments' )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(domains_router.urls)),
    path('api/', include(second_router.urls)),
]
