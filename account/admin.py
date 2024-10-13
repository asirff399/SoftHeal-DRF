from django.contrib import admin
from .models import CustomUser,Review
# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email']

    def first_name(self,obj):
        return obj.user.first_name
    
    def last_name(self,obj): 
        return obj.user.last_name
    
    def email(self,obj):
        return obj.user.email
    
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Review)