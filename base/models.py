from django.db import models
from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    points = models.IntegerField(default=0)


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date = models.DateField()
    ticket_price = models.IntegerField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    category = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=15, null=True)