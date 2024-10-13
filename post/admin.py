from django.contrib import admin
from .models import Post,PostType,Donation
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['name','image','post_type','created_on','target','collected']

class DonationAdmin(admin.ModelAdmin):
    list_display = ['user__username','post__name','donated_on','amount','balance_after_donation']

class PostTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Post,PostAdmin)
admin.site.register(PostType,PostTypeAdmin)
admin.site.register(Donation,DonationAdmin) 