from django.contrib import admin
from .models import Member, Inventory, Booking
# Register your models here.

admin.site.register(Member)
admin.site.register(Inventory)
admin.site.register(Booking)