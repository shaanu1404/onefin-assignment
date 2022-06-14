from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
import requests as Requests
from .models import Collection
from .serializers import CollectionSerializer, CreateCollectionSerializer
from .utils import get_favorite_genres


MOVIE_LIST_URL = "https://demo.credy.in/api/v1/maya/movies/"
SERVER_MOVIES_URL = 'http://localhost:8000/movies/'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movies_list(request):
    """
    GET all movies list
    """
    page = request.GET.get('page', 1)

    response = Requests.get(
        f'{MOVIE_LIST_URL}?page={page}',
        auth=(settings.MOVIE_DB_USERNAME, settings.MOVIE_DB_PASSWORD)
    )
    if response.status_code != 200:
        return Response({'message': 'Something went wrong'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    data = response.json()
    next = data.get('next')
    previous = data.get('previous')
    if next is not None:
        data['next'] = next.replace(MOVIE_LIST_URL, SERVER_MOVIES_URL)
    if previous is not None:
        data['previous'] = previous.replace(MOVIE_LIST_URL, SERVER_MOVIES_URL)
    return Response(data, status=HTTP_200_OK)


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def get_collection_list(request):
    """
    Add or Fetch collection
    """

    if request.method == 'GET':
        collections = Collection.objects.filter(user=request.user)
        get_favorite_genres(collections)
        serializer = CollectionSerializer(collections, many=True)
        return Response({
            'is_success': True,
            'data': {
                'collections': serializer.data
            }
        }, status=200)
    elif request.method == 'POST':
        serializer = CreateCollectionSerializer(
            data=request.data, context={'user': request.user})
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        collection = serializer.save()
        return Response({'collection_uuid': collection.uuid}, status=HTTP_201_CREATED)
