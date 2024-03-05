from django.contrib import admin
from .models import Person, CarAd

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'email')

admin.site.register(Person, PersonAdmin)


class CarAdAdmin(admin.ModelAdmin):
    list_display = ('code', 'url', 'title', 'price', 'year', 'mileage', 'color', 'body_status', 'modified_date')
    
admin.site.register(CarAd, CarAdAdmin)