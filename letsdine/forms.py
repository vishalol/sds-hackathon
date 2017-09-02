from mapwidgets.widgets import GooglePointFieldWidget
import re
from django import forms

#from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from dal import autocomplete
from django.urls import reverse
from django.contrib.admin import widgets




class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ( "going_time", "other_users", "food_type", "place")
        widgets = {
            'place': GooglePointFieldWidget,
            'other_users': autocomplete.ModelSelect2Multiple(url='user-autocomplete', attrs={'data-html': True}),
            
        }  
        """ 'other_users': autocomplete.ModelSelect2Multiple(url='user-autocomplete', attrs={'data-html': True}),"""      


class RegistrationForm(forms.Form):
	first_name = forms.CharField(max_length=30, label=("First Name"))
	last_name = forms.CharField(max_length=30, label=("Last Name"))
	username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))	
	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError('Username is already taken.')

	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_("The two password fields did not match."))
				return self.cleaned_data


class UserForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = '__all__'
		exclude = ('user',)				         