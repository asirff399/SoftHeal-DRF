from django.contrib import admin
from .models import Volunteer
# Register your models here.
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','gender','branch','image',]
    
admin.site.register(Volunteer,VolunteerAdmin)