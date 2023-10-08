from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer, UserRoleSerializers
from drf_spectacular.utils import extend_schema


@extend_schema(
    description="User Registration Endpoint",
    tags=["Users"],
)
class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Create role endpoint",
    tags=["Users"],
)
class CreateUserRoleAPIView(generics.CreateAPIView):
    serializer_class = UserRoleSerializers

    def post(self, request, *args, **kwargs):
        serializer = UserRoleSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
