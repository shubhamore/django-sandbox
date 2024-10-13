from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"User Registered Successfully!"}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.get(email=email)
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({"success":True,"message":"User Logged in!","refresh":str(refresh),"access":str(refresh.access_token)},status=status.HTTP_202_ACCEPTED)
        return Response({"success":False,"message":"Issue logging in with given credentials"},status=status.HTTP_400_BAD_REQUEST)
