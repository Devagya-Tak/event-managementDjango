from django.urls import path, include
from .views import hello, signup, get_events, post_events, get_tickets, post_tickets
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('hello/', hello),
    path("signup/", signup, name="signup"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/<int:pk>/', get_events, name='get_events'),
    path('events/<int:pk>/create/', post_events, name='post_events'),
    path('tickets/<int:pk>/', get_tickets, name='get_tickets'),
    path('tickets/<int:pk>/create/', post_tickets, name='post_tickets'),
]