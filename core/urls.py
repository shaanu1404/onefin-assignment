from django.urls import path
from .views import get_movies_list, get_collection_list, get_collection

urlpatterns = [
    path('movies/', get_movies_list, name="movies"),
    path('collection/', get_collection_list, name="collections"),
    path('collection/<uuid:collection_uuid>/',
         get_collection, name="single-collection"),
]
