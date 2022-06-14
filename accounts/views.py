from rest_framework_simplejwt.views import TokenObtainSlidingView
from .serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainSlidingView):
    serializer_class = MyTokenObtainPairSerializer
