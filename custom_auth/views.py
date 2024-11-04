from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view

from custom_user.models import CustomUser
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer, LogoutSerializer

from rest_framework import viewsets, status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

@extend_schema_view(create=extend_schema(exclude=True))
class RegistrationViewSet(viewsets.ViewSet):
    @extend_schema(request=UserRegistrationSerializer, responses={201: UserRegistrationSerializer})
    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def register(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LogoutSerializer,
        responses={205: 'Token successfully blacklisted', 400: 'Invalid request'}
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"detail": "Token nie został dany."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema_view(create=extend_schema(exclude=True))
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user