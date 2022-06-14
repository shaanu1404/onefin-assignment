from django.urls import path
from .views import get_movies_list, get_collection_list

urlpatterns = [
    path('movies/', get_movies_list),
    path('collection/', get_collection_list)
]
