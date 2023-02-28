from django.contrib import admin
from django.contrib.auth.models import Group
from cars.models import Services, Bookings, Cars, Reviews, Discount
# Register your models here.

admin.site.register(Services)
admin.site.register(Bookings)
admin.site.register(Cars)
admin.site.register(Reviews)
admin.site.register(Discount)

admin.site.unregister(Group)