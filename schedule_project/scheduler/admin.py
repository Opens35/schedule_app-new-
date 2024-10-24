from django.contrib import admin
from .models import Event, EventDate, Participant, Availability

# Register your models here.
admin.site.register(Event)
admin.site.register(EventDate)
admin.site.register(Participant)
admin.site.register(Availability)