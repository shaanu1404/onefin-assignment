from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_collections(request):
    return Response({'message': 'My collection data'}, status=HTTP_200_OK)
