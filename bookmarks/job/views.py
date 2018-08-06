from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from account.models import Commune, Specialite, Profile
from .forms import JobCreateForm
from django.contrib.auth.models import User
from .models import Job
from .filters import JobFilter


@login_required
def job_create(request):
    user = request.user.id
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        # form is sent
        form = JobCreateForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            form.save_m2m()
            messages.success(request, 'Job added successfully')
            # redirect to new created item detail view
    else:
        form = JobCreateForm(data=request.GET)

    return render(request, 'job/post-job.html', {'section': 'job',
                                                 'form': form,
                                                 'profile': profile})


def job_detail(request, id, slug):
    job = get_object_or_404(Job, id=id, slug=slug)
    user = get_object_or_404(User, id=job.user_id)
    return render(request,
                  'account/dashboard.html',
                  {'job': job,
                   'user': user})


def jobs(request):
    return render(request, 'job/jobs.html', {'section': 'jobs'})


def search(request):
    projects_list = Job.objects.filter(status='published')
    projects_pagination = JobFilter(request.GET, queryset=projects_list)
    paginator = Paginator(projects_pagination.qs, 1)  # 3 Projects in each page
    page = request.GET.get('page')
    try:
        projects_filter = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        projects_filter = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        projects_filter = paginator.page(paginator.num_pages)
    return render(request, 'job/jobs.html', {'projects_filter': projects_filter,
                                             'filter': projects_pagination,
                                             'page': page})
