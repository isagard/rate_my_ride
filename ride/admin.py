from django.contrib import admin
from ride.models import Review, ServicePage
from ride.models import UserProfile 

class ServicePageAdmin(admin.ModelAdmin):
    list_display = ('serviceID','name', 'location', 'body')

class ReviewAdmin(admin.ModelAdmin):
    prepopulated_fields = {'service':('location',)}

# Register your models here.
admin.site.register(ServicePage, ServicePageAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)
