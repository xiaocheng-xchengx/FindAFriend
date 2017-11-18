from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views
from findafriend.views import home, signup, deleteUser, chatDirect
from rest_framework import routers
from .views import PageDetail, PageSearch, PageRetrieve, ProfileViewSet, ProfileAPIView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
	url(r'^pageSearch/$', PageSearch.as_view(), name='list'),
	url(r'^pageDetail/$', PageDetail.as_view(), name='detail'),
	url(r'^retrieve/(?P<title>[\w|\W]+)/$', PageRetrieve.as_view(), name='retrieve'),
	url(r'^profiles/(?P<user>[\w|\W]+)/$', ProfileAPIView.as_view(), name='profiles'),

]


#urlpatterns=format_suffix_patterns(urlpatterns) 