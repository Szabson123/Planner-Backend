from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(create=extend_schema(exclude=True))
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
