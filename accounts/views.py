from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer, UserLoginSerializer, UserRoleSerializers
from .validation import (
    validate_password_field,
    validate_user_registration_data,
    is_email_already_registered,
    is_username_already_taken,
    validate_username_field,
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
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            username_error = e.detail.get("username")
            password_error = e.detail.get("password")

            if username_error:
                return Response(
                    {"error": "Username may not be blank."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if password_error:
                return Response(
                    {"error": "Password may not be blank."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        # Validate user inputs
        if validate_username_field(username):
            return Response(
                {"error": "Your login attempt was unsuccessful. Please try again."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        if validate_password_field(password, password):
            return Response(
                {"error": "Your login attempt was unsuccessful. Please try again."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                "access_token": str(refresh.access_token),
                # "user": CustomUserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
