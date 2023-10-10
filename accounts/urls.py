from django.urls import path
from .views import UserCreateAPIView, CreateUserRoleAPIView, UserLoginAPIView

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="user-create"),
    path("role/", CreateUserRoleAPIView.as_view(), name="user-role"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
]
