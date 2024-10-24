from django.db import models
from accounts.models import User
from django.utils import timezone
# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True)

class EventDate(models.Model):
    event = models.ForeignKey(Event, related_name="dates", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)


class Participant(models.Model):
    event = models.ForeignKey(Event, related_name='participants', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

class Availability(models.Model):
    participant = models.ForeignKey(Participant, related_name='availabilities', on_delete=models.CASCADE)
    event_date = models.ForeignKey(EventDate, on_delete=models.CASCADE)
    availability = models.CharField(max_length=10, choices=[
        ('yes', '〇'),
        ('maybe', '△'),
        ('no', '×'),
    ])

# class Participant(models.Model):
#     availability_choices = [
#         ('yes', '〇'),
#         ('maybe', '△'),
#         ('no', '×'),
#     ]
#     event = models.ForeignKey(Event, related_name="participants", on_delete=models.CASCADE)
#     name = models.CharField(max_length=100, blank=True)
#     availability = models.CharField(max_length=5, choices=availability_choices)
#     comment = models.TextField(blank=True, null=True)