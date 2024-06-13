from django.shortcuts import render
from rest_framework.decorators  import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import CustomUser


@api_view(['GET'])
def hello(request):
    return Response({
        "message": "Hello World"
    })

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Make sure to call save() method
        return Response({
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_events(request, pk):
    user=pk
    try:
        events = Event.objects.filter(user=user) 
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response({"message": "Event not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def post_events(request, pk):
    request.data['user'] = pk
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Make sure to call save() method
        return Response({
            "message": "Event created successfully"
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_tickets(request, pk):
    user = pk
    tickets = Ticket.objects.filter(user=user)
    
    if not tickets.exists():  # Check if tickets exist for the user
        return Response({"message": "No tickets found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_tickets(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)  # Assuming you have a User model
    except CustomUser.DoesNotExist:
        return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    request.data['user'] = user.id
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "ticket created successfully"
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def earn_points(request):
    user_id = request.data['user']
    points_to_give = request.data['points']


    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({
            'error': 'User not found'
        },  status=404)
    
    user.points += points_to_give
    user.save()

    return Response({
        'message': 'Points erned successfuly'
    })

    
