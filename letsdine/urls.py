from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

app_name = 'letsdine'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'letsdine/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^addplan/$', views.add_plan, name='add_plan'),
    url(r'^editprofile/$', views.edit_profile, name='editprofile'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^cancelplan/(?P<plan_id>[0-9]+)/$', views.cancelplan, name='cancelplan'),
    url(r'^confirmplan/(?P<plan_id>[0-9]+)/$', views.confirmplan, name='confirmplan'),
    url(r'^requestplan/(?P<plan_id>[0-9]+)/$', views.requestplan, name='requestplan'),
]