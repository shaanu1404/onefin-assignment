from django.urls import path
from .views import MyTokenObtainPairView, request_counter, request_counter_reset


urlpatterns = [
    path('register/', MyTokenObtainPairView.as_view()),
    path('request-count/', request_counter),
    path('request-count/reset/', request_counter_reset),
]
