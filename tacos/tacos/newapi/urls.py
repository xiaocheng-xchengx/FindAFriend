from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views
from rest_framework import routers
from .views import ProfileViewSet, ProfileAPIView, UserCreateAPIView, UserLoginAPIView, PageCreateAPIView
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ProfileUpdateView

urlpatterns = [
	url(r'^api/profile/update/$', ProfileUpdateView.as_view(), name='update'),
	url(r'^api/profiles/$', ProfileAPIView.as_view(), name='profiles'),
	url(r'^api/login/$', UserLoginAPIView.as_view(), name='login'),
 	url(r'^api/register/$', UserCreateAPIView.as_view(), name='register'),
 	url(r'^api/pageCreate/$', PageCreateAPIView.as_view(), name='pagecreate'),
]


#urlpatterns=format_suffix_patterns(urlpatterns) 
