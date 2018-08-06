from django.urls import path, re_path
from job import views

app_name = 'job'

urlpatterns = [

    path('', views.jobs, name="jobs"),
    path('post/', views.job_create, name="job-add"),
    re_path(r'^job/detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.job_detail, name='job-detail'),
    path('search/', views.search, name='jobs-search'),
]
