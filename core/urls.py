from django.urls import path
from .views import get_all_collections

urlpatterns = [
    path('collection/', get_all_collections)
]
