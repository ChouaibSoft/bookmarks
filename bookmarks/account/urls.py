import django
from django.contrib.auth.views import login
from django.urls import path, re_path
from account import views
from django.views.i18n import JavaScriptCatalog



urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('index/', views.index_page, name="index-page"),
    path('register/', views.register, name="register"),
    path('profile/add/', views.profile_create, name="profile-add"),
    re_path(r'^profile/update/(?P<id>\d+)/$', views.profile_update, name="profile-update"),
    path('projects/', views.my_projects, name="my-projects"),
    re_path(r'^update/(?P<id>\d+)/$', views.user_update, name="user-update"),
    re_path(r'^condidates/$', views.search, name='condidates'),
    re_path(r'^condidate/profile/(?P<id>\d+)/(?P<username>[-\w]+)/$', views.condidate_detail, name='condidate_detail'),
    path('login/', django.contrib.auth.views.login, name="login"),
    re_path(r'^like/$', views.profile_like, name='like'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('ajax/validate_email/', views.validate_email, name='validate_email'),
    path('logout/', django.contrib.auth.views.logout, name='logout'),
    path('logout-then-login/', django.contrib.auth.views.login, name='logout-then-login'),
    path('ajax/load-communes/', views.load_communes, name='ajax_load_communes'),
    path('ajax/load-specialites/', views.load_specialites, name='ajax_load_specialites'),
    path(r'jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

