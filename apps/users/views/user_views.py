from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.serializers.user_serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.contrib.auth import authenticate


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


def set_jwt_cookies(response, user):
    """
    Сохранение токенов для передачи в запросы
    """
    # Создаем новый RefreshToken для пользователя
    refresh = RefreshToken.for_user(user)

    # Явно создаем AccessToken из RefreshToken
    access_token = AccessToken.for_user(user)

    # Преобразуем токены в строки для установки в куки
    access_token_str = str(access_token)
    refresh_token_str = str(refresh)

    # Получаем время истечения для access и refresh токенов
    access_expiry = datetime.utcfromtimestamp(access_token['exp'])
    refresh_expiry = datetime.utcfromtimestamp(refresh['exp'])

    response = Response(status=status.HTTP_200_OK)
    response.set_cookie(
        key='access_token',
        value=access_token_str,
        httponly=True,
        secure=False,  # Используйте True для HTTPS
        samesite='Lax',
        expires=access_expiry
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token_str,
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_expiry
    )


class RegisterUserGenericView(generics.CreateAPIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
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


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Используем exp для установки времени истечения куки
            access_expiry = datetime.utcfromtimestamp(access_token['exp'])
            refresh_expiry = datetime.utcfromtimestamp(refresh['exp'])

            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False,  # Используйте True для HTTPS
                samesite='Lax',
                expires=access_expiry
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry
            )
            return response
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class ProtectedDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, authenticated user!", "user": request.user.username})
