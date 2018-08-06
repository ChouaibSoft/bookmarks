from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from account.models import Commune, Specialite, Profile
from .forms import ProjectCreateForm
from django.contrib.auth.models import User
from .models import Project
from .filters import JobFilter



@login_required
def project_create(request):
    user = request.user.id
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        # form is sent
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            form.save_m2m()
            messages.success(request, 'Job added successfully')
            redirect("my-projects")
    else:
        form = ProjectCreateForm(data=request.GET)

    return render(request, 'project/post-project.html', {'section': 'project',
                                                 'form': form,
                                                 'profile': profile})

@login_required
def project_detail(request, id, slug):
    user = request.user.id
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    project = get_object_or_404(Project, id=id, slug=slug)
    return render(request,
                  'account/project-detail.html',
                  {'project': project,
                   'profile': profile})


@login_required
def project_update(request, id):
    user = request.user.id
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    job = get_object_or_404(Project, id=id)

    form = ProjectCreateForm(request.POST or None, instance=job)
    if form.is_valid():
        job.save()
        print("This project is updated")

    return render(request, 'project/project_update.html', {'form': form, 'project': job, 'profile': profile})


@login_required
def project_delete(request, id):
    user = request.user.id
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    job = get_object_or_404(Project, id=id)
    if request.method == "post":
        job.delete()
        print("This project was deleted !")
        redirect("dashboard")

    return render(request, 'project/project_delete.html', {'project': job, 'profile': profile})



def search(request):
    projects_list = Project.objects.filter(status='published')
    projects_pagination = JobFilter(request.GET, queryset=projects_list)
    paginator = Paginator(projects_pagination.qs, 6)  # 3 Projects in each page
    page = request.GET.get('page')
    try:
        projects_filter = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        projects_filter = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        projects_filter = paginator.page(paginator.num_pages)
    return render(request, 'project/projects.html', {'projects_filter': projects_filter,
                                             'filter': projects_pagination,
                                             'page': page})



@login_required
@require_POST
def project_follow(request):
    project_id = request.POST.get('id')
    action = request.POST.get('action')
    if project_id and action:
        try:
            project= Project.objects.get(id=project_id)
            if action == 'follow':
                project.users_follow.add(request.user)
            else:
                project.users_follow.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})