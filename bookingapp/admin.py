from django.contrib import admin
from .models import Member, Inventory, Booking, MemberAdmin, InventoryAdmin, BookingAdmin
# Register your models here.

admin.site.register(Member, MemberAdmin)
admin.site.register(Inventory,InventoryAdmin)
admin.site.register(Booking, BookingAdmin)