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
from datetime import datetime, timedelta
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from dal import autocomplete
from geopy.geocoders import GoogleV3, Nominatim

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
    myplans = request.user.iplans.all().order_by('-created_on')[:5]
    planr = request.user.iplans.all().order_by('-created_on')
    requestlist = []
    recentrequestlist = []
    for plan in planr:
        pl = Plan_request.objects.filter(plan=plan)
        for p in pl:
            requestlist.append(p)
    recentrequestlist = sorted(requestlist, key=lambda x: x.created_on, reverse=True)

    geolocator = GoogleV3()
    mypostlist = []
    for plan in myplans:
        x = str(plan.place.x)
        a = plan.place.x
        b = plan.place.y
        y = str(plan.place.y)
        location = geolocator.reverse((b,a))
        mypostlist.append(location[0])
        print location[0]
    user = request.user
    logg = UserProfile.objects.get(user=request.user)
    latest_plans = Plan.objects.order_by('-created_on')[:5]
    geolocator = Nominatim()
    postlist = []
    for plan in latest_plans:
        x = str(plan.place.x)
        a = plan.place.x
        b = plan.place.y

        y = str(plan.place.y)
        location = geolocator.reverse((b,a))
        postlist.append(location)
    print recentrequestlist
    context = {
    'userp' : logg,
    'user' : user,
    'plans' : latest_plans,
    'planz': zip(latest_plans, postlist),
    'myplanz': zip(myplans, mypostlist),
    'recentrequestlist':recentrequestlist,
    }
    return render(request, 'letsdine/dashboard.html', context)


@login_required(login_url='/login')
def edit_profile(request):
    myplans = request.user.iplans.all().order_by('-created_on')[:5]        
    geolocator = Nominatim()
    mypostlist = []
    for plan in myplans:
        x = str(plan.place.x)
        a = plan.place.x
        b = plan.place.y
        y = str(plan.place.y)
        location = geolocator.reverse((b,a))
        mypostlist.append(location)
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
            'myplanz': zip(myplans, mypostlist),
            
            }   
            return HttpResponseRedirect(reverse('letsdine:editprofile'), context)
        else :
            context = {
            'user' : user,
            'profile' : profile,
            'form'  : form,
            'myplanz': zip(myplans, mypostlist)
            } 
            return HttpResponseRedirect(reverse('letsdine:editprofile'), context)
    else:    
        user = User.objects.get(username= request.user.username)
        profile = UserProfile.objects.get(user = request.user)
        form = UserForm(request.POST, instance=profile)
        context = {
            'user' : user,
            'profile' : profile,
            'form'  : form,
            'myplanz': zip(myplans, mypostlist)
        }
        return render(request, 'letsdine/editprofile.html', context) 

@login_required(login_url='/login')
def profile(request, username):
    myplans = request.user.iplans.all().order_by('-created_on')[:5]
    geolocator = Nominatim()
    mypostlist = []
    for plan in myplans:
        x = str(plan.place.x)
        a = plan.place.x
        b = plan.place.y
        y = str(plan.place.y)
        location = geolocator.reverse((b,a))
        mypostlist.append(location)
    logg = UserProfile.objects.get(user=request.user)
    loguser = request.user
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    context = {
    'user' : user,
    'userp' : profile,
    'loguser' : loguser,
    'myplanz': zip(myplans, mypostlist)
    }
    return render(request, 'letsdine/prof.html', context)


@login_required(login_url='/login')
def add_plan(request):
    myplans = request.user.iplans.all().order_by('-created_on')[:5]
    geolocator = Nominatim()
    mypostlist = []
    for plan in myplans:
        x = str(plan.place.x)
        a = plan.place.x
        b = plan.place.y
        y = str(plan.place.y)
        location = geolocator.reverse((b,a))
        mypostlist.append(location)
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
        'myplanz': zip(myplans, mypostlist)
        }
            return render(request, 'letsdine/create.html', context)
    else:
        logg = UserProfile.objects.get(user=request.user)
        form = PlanForm()
        context = {
        'form': form,
        'logg' : logg,
        'myplanz': zip(myplans, mypostlist)
        }   
        return render(request, 'letsdine/create.html', context)


@login_required(login_url='/login')
def cancelplan(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    user = request.user 
    plan.other_users.remove(request.user)
    if plan.other_users.count()==0:
        Plan.objects.filter(id = plan_id).delete()
    return HttpResponseRedirect(reverse('letsdine:dashboard'))


@login_required(login_url='/login')
def requestplan(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    user = request.user 
    Plan_request.objects.create(user=user, plan=plan )
    return HttpResponseRedirect(reverse('letsdine:dashboard')) 

@login_required(login_url='/login')
def confirmplan(request, plan_id):
    planreq = get_object_or_404(Plan_request, pk=plan_id)
    plan = planreq.plan
    if not planreq.user in plan.other_users.all():
        plan.other_users.add(planreq.user)
    Plan_request.objects.filter(id=plan_id).delete()    
    return HttpResponseRedirect(reverse('letsdine:dashboard'))

@login_required(login_url='/login')
def rejectplan(request, plan_id):
    Plan_request.objects.filter(id=plan_id).delete()
    return HttpResponseRedirect(reverse('letsdine:dashboard')) 
from django.utils import timezone


@login_required(login_url='/login')
def search(request):
    myplans = request.user.iplans.all().order_by('-created_on')[:5]
    geolocator = Nominatim()
    mypostlist = []
    for plan in myplans:
        x = str(plan.place.x)
        a = plan.place.x
        b = plan.place.y
        y = str(plan.place.y)
        location = geolocator.reverse((b,a))
        mypostlist.append(location)
    if request.method == 'GET':
        allplan = Plan.objects.all()
        query_time= request.GET.get('time')

        query_type= request.GET.get('type', "None")
        if query_time and query_type:
            query_time = datetime.strptime(query_time, "%Y-%m-%d %H:%M:%S")
            start = query_time - timedelta(hours = 1)
            end = query_time + timedelta(hours = 1)
            start = timezone.make_aware(start, timezone.get_current_timezone())
            end = timezone.make_aware(end, timezone.get_current_timezone())
            qs = Plan.objects.filter(created_on__range=(start, end))
            qs = qs.filter(food_type = query_type)
        if query_time and not query_type:
            query_time = datetime.strptime(query_time, "%Y-%m-%d %H:%M:%S")
            start = query_time - timedelta(hours = 1)
            end = query_time + timedelta(hours = 1)
            start = timezone.make_aware(start, timezone.get_current_timezone())
            end = timezone.make_aware(end, timezone.get_current_timezone())
            qs = Plan.objects.filter(created_on__range=(start, end)) 
        if query_type and not query_time:
            qs = Plan.objects.filter(food_type = query_type)
        geolocator = Nominatim()
        qpostlist = []
        for plan in qs:
            x = str(plan.place.x)
            a = plan.place.x
            b = plan.place.y
            print x

            y = str(plan.place.y)
            print y
            location = geolocator.reverse((a,b))
            qpostlist.append(location)    
        context = {
        'myplanz': zip(myplans, mypostlist),
        'qs' : qs,
        'searched': zip(qs,qpostlist )
        }     
        return render(request, 'letsdine/Search.html', context)       

    context = {
        'myplanz': zip(myplans, mypostlist)
        }     
    return render(request, 'letsdine/Search.html', context)


