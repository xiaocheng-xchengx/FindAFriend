from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views
from rest_framework import routers
from tacos.newapi import views
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/pages', views.PageViewSet)
router.register(r'api/profiles', views.ProfileViewSet)
router.register(r'api/messages', views.ChatViewSet)
router.register(r'api/joinGroup/(?P<group>.+)/(?P<username>.+)', views.JoinGroupSet)
router.register(r'api/leaveGroup/(?P<group>.+)/(?P<username>.+)', views.LeaveGroupSet)
router.register(r'api/deleteGroup/(?P<group>.+)', views.DeleteGroupSet)
router.register(r'api/updateGroup/(?P<group>.+)/(?P<description>.+)/(?P<type>.+)', views.UpdateGroupSet)
router.register(r'api/updateProfile/(?P<user>.+)/(?P<first_name>.+)/(?P<last_name>.+)/(?P<hometown>.+)/(?P<university>.+)/(?P<picture>.+)', views.UpdateProfile)
router.register(r'api/deleteUser/(?P<user>.+)', views.DeleteUser)





urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include('tacos.newapi.urls')),


    ]

#urlpatterns = format_suffix_patterns(urlpatterns)
