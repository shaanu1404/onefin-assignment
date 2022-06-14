from django.urls import path
from .views import get_movies_list

urlpatterns = [
    path('movies/', get_movies_list)
]
