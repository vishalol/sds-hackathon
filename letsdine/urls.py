from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

app_name = 'letsdine'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^addplan/$', views.add_plan, name='add_plan'),
]