from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.views import TokenObtainSlidingView
from .serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainSlidingView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def request_counter(request):
    count = request.session.get('REQUEST_COUNT', 0)
    return Response({'requests': count}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_counter_reset(request):
    request.session['REQUEST_COUNT'] = 0
    return Response({'message': 'Request count reset successfully'}, status=HTTP_200_OK)
