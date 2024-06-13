from django.contrib import admin
from .models import Ticket, Event, CustomUser
# Register your models here.

admin.site.register(Ticket)
admin.site.register(Event)
admin.site.register(CustomUser)