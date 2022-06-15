from django.conf import settings
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT
)
import requests as Requests
from .models import Collection
from .serializers import DataCollectionSerializer, CollectionSerializer
from .utils import get_favorite_genres


MOVIE_LIST_URL = "https://demo.credy.in/api/v1/maya/movies/"


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
        return Response({'error': response.reason}, status=response.status_code)

    data = response.json()
    next = data.get('next')
    previous = data.get('previous')
    movies_abs_uri = request.build_absolute_uri(reverse('movies'))
    if next is not None:
        data['next'] = next.replace(MOVIE_LIST_URL, movies_abs_uri)
    if previous is not None:
        data['previous'] = previous.replace(MOVIE_LIST_URL, movies_abs_uri)
    return Response(data, status=HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_collection_list(request):
    """
    GET all collections or POST a collection
    """

    if request.method == 'GET':
        collections = Collection.objects.filter(user=request.user)
        favorite_genres = get_favorite_genres(collections)
        serializer = DataCollectionSerializer(collections, many=True)
        return Response({
            'is_success': True,
            'data': {
                'collections': serializer.data,
                'favourite_genres': ",".join(favorite_genres)
            }
        }, status=200)

    elif request.method == 'POST':
        serializer = CollectionSerializer(
            data=request.data, context={'user': request.user})

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        collection = serializer.save()
        return Response({'collection_uuid': collection.uuid}, status=HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def get_collection(request, collection_uuid):
    """
    GET single collection by id or DELETE collection or PUT collection
    """

    if request.method == 'GET':
        try:
            collection = Collection.objects.get(uuid=collection_uuid)
            serializer = CollectionSerializer(collection)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            collection = Collection.objects.get(uuid=collection_uuid)
            collection.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':

        try:
            collection = Collection.objects.get(uuid=collection_uuid)
            serializer = CollectionSerializer(
                instance=collection, data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'message': 'Collection updated successfully'}, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
