from django.urls import path, re_path
from project import views

app_name = 'project'

urlpatterns = [

    path('add/', views.project_create, name="project-add"),
    re_path(r'^detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.project_detail, name='project-detail'),
    re_path(r'^update/(?P<id>\d+)/$', views.project_update, name="project-update"),
    re_path(r'^delete/(?P<id>\d+)/$', views.project_delete, name="project-delete"),
    re_path(r'^follow/$', views.project_follow, name='follow'),
    path('search/', views.search, name='projects-search'),
]
