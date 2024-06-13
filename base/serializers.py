from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Event, Ticket, CustomUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'