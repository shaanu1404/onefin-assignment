from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
import requests as Requests
from django.conf import settings

MOVIE_LIST_URL = "https://demo.credy.in/api/v1/maya/movies/"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movies_list(request):
    response = Requests.get(
        MOVIE_LIST_URL,
        auth=(settings.MOVIE_DB_USERNAME, settings.MOVIE_DB_PASSWORD)
    )
    if response.status_code != 200:
        return Response({'message': 'Something went wrong'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    data = response.json()
    return Response(data, status=HTTP_200_OK)
