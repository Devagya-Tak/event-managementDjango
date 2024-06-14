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
        # Retrieve the user based on the provided primary key
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        # Return a response if the user does not exist
        return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the event ID from the request data
    event_id = request.data.get('event')
    try:
        # Attempt to retrieve the event based on the provided ID
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        # Return a response if the event does not exist
        return Response({'message': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the payment method is via points
    payment_method = request.data.get('payment_method')
    if payment_method == 'points':
        # Calculate the points needed based on the ticket price
        points_needed = event.ticket_price * 20
        if user.points >= points_needed:
            # Deduct points from the user's account if they have sufficient points
            user.points -= points_needed
            user.save()
        else:
            # Return a response if the user has insufficient points
            return Response({"message": "Insufficient points"}, status=status.HTTP_400_BAD_REQUEST)

    # Assign the user ID to the request data
    request.data['user'] = user.id
    # Initialize the serializer with the request data
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        # Save the ticket if the serializer data is valid
        serializer.save()
        # Return a success response
        return Response({
            "message": "Ticket created successfully"
        }, status=status.HTTP_201_CREATED)
    else:
        # Return a response with errors if the serializer data is invalid
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

    
