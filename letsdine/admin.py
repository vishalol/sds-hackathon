from django.contrib import admin
from .forms import *
# Register your models here.\
from .models import *

admin.site.register(UserProfile)

admin.site.register(Plan_request)
admin.site.register(Intrest)
admin.site.register(Message)


from mapwidgets.widgets import GooglePointFieldWidget

class PlanAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
admin.site.register(Plan, PlanAdmin)