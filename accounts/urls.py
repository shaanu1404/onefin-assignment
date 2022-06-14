from django.urls import path
from .views import MyTokenObtainPairView


urlpatterns = [
    path('register/', MyTokenObtainPairView.as_view())
]
