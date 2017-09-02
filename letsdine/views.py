from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q 
from django.urls import reverse
from django.views import generic
from .forms import *
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from dal import autocomplete

# Create your views here.

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        query = UserProfile.objects.all()
        qs = []
        for userp in query:
            qs.append(userp.user)

        if self.q:
            qs = qs.filter( Q(username__icontains = self.q))
        return qs

@csrf_protect 
def register(request):
    if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('letsdine:dashboard'))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            user = User.objects.get(username=form.cleaned_data['username'])
            profile = UserProfile.objects.create(
                user = user
            )
            login(request, user)
            return HttpResponseRedirect(reverse('letsdine:dashboard'))
        else :
            context = {
            'form': form
             } 
            return render(request, 'letsdine/register.html', context)
    else:
        form = RegistrationForm()
        context = {
        'form': form
        }   
        return render(request, 'letsdine/register.html', context)

def index(request):
    return render(request, 'letsdine/index.html')

@login_required(login_url='/login')
def dashboard(request):
    user = request.user
    logg = UserProfile.objects.get(user=request.user)
    latest_plans = Plan.objects.order_by('-created_on')[:5]   
    context = {
    'userp' : logg,
    'user' : user,
    'plans' : latest_plans,
    }
    return render(request, 'letsdine/dashboard.html', context)


@login_required(login_url='/login')
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = UserProfile.objects.get(user=user)
        form = UserForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            form.save_m2m()
            context = {
            'user' : user,
            'profile' : profile,
            'form'  : form,
            }   
            return HttpResponseRedirect(reverse('letsdine:edit_profile'), context)
        else :
            context = {
            'user' : user,
            'profile' : profile,
            'form'  : form,
            } 
            return HttpResponseRedirect(reverse('letsdine:edit_profile'), context)
    else:    
        user = User.objects.get(username= request.user.username)
        profile = UserProfile.objects.get(user = request.user)
        form = UserForm(request.POST, instance=profile)
        context = {
            'user' : user,
            'profile' : profile,
            'form'  : form,
            'logg' : logg,
        }
        return render(request, 'letsdine/user.html', context) 

@login_required(login_url='/login')
def profile(request, username):
    logg = UserProfile.objects.get(user=request.user)
    loguser = request.user
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    context = {
    'user' : user,
    'userp' : profile,
    'loguser' : loguser,
    }
    return render(request, 'letsdine/userprofile.html', context)


@login_required(login_url='/login')
def add_plan(request):
    logg = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = PlanForm(request.POST)
        user = request.user
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
            form.save_m2m()
            if not user in f.other_users.all():
                f.other_users.add(request.user)
                f.save()  
            return HttpResponseRedirect(reverse('letsdine:dashboard'))
        else :
            context = {
        'form': form,
        'logg' : logg,
        }
            return render(request, 'letsdine/plan.html', context)
    else:
        logg = UserProfile.objects.get(user=request.user)
        form = PlanForm()
        context = {
        'form': form,
        'logg' : logg,
        }   
        return render(request, 'letsdine/plan.html', context)                                  
