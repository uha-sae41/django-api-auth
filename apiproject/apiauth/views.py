from faulthandler import is_enabled

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .Serializer import AuthSerializer
from .models import CustomUser

class isBanquier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'banquier' or request.user.role == 'administrateur'

class PermissionSelfOrBanquier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'banquier' or request.user.role == 'administrateur' or request.user.id == view.kwargs.get('id')

class PermissionBanquier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'banquier'

class PermissionSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.id == view.kwargs.get('id')

class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated, isBanquier]

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = AuthSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = AuthSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = AuthSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = AuthSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, PermissionSelf]

    def put(self, request, *args, **kwargs):
        id = request.data.get('user_id')
        user = CustomUser.objects.get(id=id)

        email = request.data.get('email')
        if email is not None:
            data = {'email': email}
        else:
            data = {}

        serializer = AuthSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateViewByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated, PermissionBanquier]

    def put(self, request, id, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AuthSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ValidateTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        token = None

        if auth_header and auth_header.startswith('Token '):
            token = auth_header.split(' ')[1]

        if not token:
            token = request.data.get('token')

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
            serializer = AuthSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated, isBanquier]

    def get(self, request, id, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=id)
            serializer = AuthSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)