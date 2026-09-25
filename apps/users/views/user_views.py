from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.serializers.user_serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timezone
from django.contrib.auth import authenticate
from rest_framework import serializers
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

def set_jwt_cookies(response, user):
    """
    Створює JWT і додає їх до HttpOnly cookies.
    """
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    access_expiry = datetime.fromtimestamp(access_token['exp'],tz=timezone.utc,)
    refresh_expiry = datetime.fromtimestamp(refresh_token['exp'],tz=timezone.utc,)

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,  # Для локальної розробки; у production має бути True
        samesite='Lax',
        expires=access_expiry,
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_expiry,
    )

    return response


class RegisterUserGenericView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = Response({
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
            set_jwt_cookies(response, user)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # USERNAME_FIELD у моделі User дорівнює "email"
        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user is None:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            },
            status=status.HTTP_200_OK,
        )

        return set_jwt_cookies(response, user)


class LogoutView(APIView):

    @extend_schema(
        request=None,
        responses={
            204: OpenApiResponse(
                description='JWT cookies deleted successfully.'
            ),
        },
    )

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class ProtectedDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='ProtectedDataResponse',
                fields={
                    'message': serializers.CharField(),
                    'user': serializers.CharField(),
                },
            ),
        },
    )

    def get(self, request):
        return Response({
            "message": "Hello, authenticated user!",
            "user": request.user.username})
