from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Profile
from project.models import Project
from account.models import Commune, Specialite
from .forms import UserRegistrationForm, ProfileCreateForm, UserEditForm
from .filters import CondidateFilter
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def index_page(request):
    condidates = Profile.objects.filter(wilaya=1)[:5]
    return render(request, "index.html", {'condidates': condidates})


@login_required
def dashboard(request):
    user = request.user.id
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if profile:
        projects = Project.objects.filter(categorie=profile.categorie, wilaya=profile.wilaya, status="published")
        paginator = Paginator(projects, 5)
        page = request.GET.get('page')
        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            projects = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                # If the request is AJAX and the page is out of range return an empty page
                return HttpResponse('')
            # If page is out of range deliver last page of results
            projects = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request,
                          'account/jobs-ajax.html',
                          {'section': 'projects',
                           'projects': projects,
                           'user':user,
                           'profile': profile})
        return render(request, 'account/dashboard.html',{
                             'profile': profile,
                             'projects': projects})

    else:
        return render(request, 'account/dashboard.html')




@login_required
def profile_create(request):
    if request.method == 'POST':
        # form is sent
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        form = ProfileCreateForm(request.POST, request.FILES)
        if form.is_valid() and user_form.is_valid():
            user_form.save()
            new_item = form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            form.save_m2m()
            messages.success(request, 'Profile added successfully')
            # redirect to new created item detail view
    else:
        user_form = UserEditForm(instance=request.user)
        form = ProfileCreateForm(data=request.GET)

    return render(request, 'account/profile-add.html', {'user_form': user_form,
                                                        'section': 'profile',
                                                        'form': form})


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


@login_required
def profile_update(request, id):
    profile = get_object_or_404(Profile, id=id)
    user_form = UserEditForm(instance=request.user,
                             data=request.POST)
    form = ProfileCreateForm(request.POST or None, instance=profile)
    if form.is_valid():
        profile.save()
        print("This account is updated")

    return render(request, 'account/profile-update.html', {'user_form': user_form, 'form': form, 'profile': profile})


@login_required
def user_update(request, id):
    user = get_object_or_404(User, id=id)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    form = UserRegistrationForm(request.POST or None, instance=user)
    if form.is_valid():
        user.save()
        print("This account is updated")

    return render(request, 'account/user-update.html', {'form': form, 'user': user, 'profile':profile})

def load_communes(request):
    wilaya_id = request.GET.get('wilaya')
    communes = Commune.objects.filter(wilaya_id=wilaya_id).order_by('name')
    return render(request, 'account/commune_dropdown_list_options.html', {'communes': communes})


def load_specialites(request):
    categorie_id = request.GET.get('categorie')
    specialites = Specialite.objects.filter(categorie_id=categorie_id).order_by('name')
    return render(request, 'account/specialite_dropdown_list_options.html', {'specialites': specialites})


def search(request):
    condidate_list = Profile.objects.all()
    condidates_pagination = CondidateFilter(request.GET, queryset=condidate_list)
    paginator = Paginator(condidates_pagination.qs, 6)  # 3 Projects in each page
    page = request.GET.get('page')
    try:
        condidates_filter = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        condidates_filter = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        condidates_filter = paginator.page(paginator.num_pages)
    return render(request, 'account/condidates.html', {'condidates_filter': condidates_filter,
                                                       'filter': condidates_pagination,
                                                       'page': page})



def condidate_detail(request, id, username):
    condidate = get_object_or_404(Profile, id=id)
    user = get_object_or_404(User, id=condidate.user_id)
    return render(request,
                  'account/condidate-detail.html',
                  {'condidate': condidate,
                   'user': user})

@login_required
def my_projects(request):
    user = request.user.id
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    projects = Project.objects.filter(user_id=user)


    return render(request, 'account/my-project.html', {'projects': projects, 'profile': profile})



@login_required
@require_POST
def profile_like(request):
    profile_id = request.POST.get('id')
    action = request.POST.get('action')
    if profile_id and action:
        try:
            profile = Profile.objects.get(id=profile_id)
            if action == 'like':
                profile.users_like.add(request.user)
            else:
                profile.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})