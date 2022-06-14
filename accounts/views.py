from rest_framework_simplejwt.views import TokenObtainSlidingView
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer


class MyTokenObtainPairSerializer(TokenObtainSlidingSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data = {'access_token': data['token']}
        return data


class MyTokenObtainPairView(TokenObtainSlidingView):
    serializer_class = MyTokenObtainPairSerializer
