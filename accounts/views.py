from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer, UserLoginSerializer, UserRoleSerializers
from .validation import (
    validate_user_registration_data,
    is_email_already_registered,
    is_username_already_taken,
)
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken


@extend_schema(
    description="User Registration Endpoint",
    tags=["Users"],
)
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        data = request.data
        validation_response = validate_user_registration_data(data)

        if validation_response:
            return validation_response

        email = data.get("email")
        username = data.get("username")

        if is_email_already_registered(email):
            return Response(
                {"error": "Email already registered."}, status=status.HTTP_409_CONFLICT
            )

        if is_username_already_taken(username):
            return Response(
                {"error": "Username already taken."}, status=status.HTTP_409_CONFLICT
            )

        # Create the user After validation
        User = get_user_model()
        User.objects.create_user(
            email=email,
            username=username,
            password=data.get("password"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
        )
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )


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


@extend_schema(
    description="User Sign-In (Login) Endpoint",
    tags=["Users"],
)
class UserLoginAPIView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )
