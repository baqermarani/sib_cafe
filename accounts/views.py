from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from .serializers import UserRegisterSerializer, UserSerializer, UserLoginSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()

    def list(self, request):
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)  # get user by id
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)  # get user by id
        if user != request.user:
            return Response({'massage': 'You are not authorized to update this user'})
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({'massage': 'You are not authorized to update this user'})
        user.is_active = False
        user.save()
        return Response({'massage': 'User deleted successfully'})


class RegisterView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'personal_id': serializer.data['personal_id']
                }
            }

            return Response(response, status=status_code)

