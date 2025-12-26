from django.contrib import admin
from .models import Contact, CareerApplication

admin.site.register(Contact)


@admin.register(CareerApplication)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'position', 'applied_at')