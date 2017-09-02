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
