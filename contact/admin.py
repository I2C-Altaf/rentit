from django.contrib import admin
from contact.models import Contact
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ('email','subject','contacted_on')

admin.site.register(Contact, ContactAdmin)