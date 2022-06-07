from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework import permissions
from .models import MyUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class CreateAccount(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        reg_serializer = RegistrationSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response({"message": "Signup successfully"}, status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        params = request.data
        if params["email"] is None or params["password"] is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=params["email"], password=params["password"])
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "message": "Login Successfully."}, status=status.HTTP_200_OK)


class ListUsers(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegistrationSerializer

    def get(self, request):
        instance = MyUser.objects.all()
        serializers = self.serializer_class(instance, many=True)
        return Response({"message": "Getting all records.", "data": serializers.data}, status=status.HTTP_200_OK)


class UpdateProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegistrationSerializer

    def put(self, request):
        params = request.data
        print(request.user)
        instance = MyUser.objects.get(email=request.user)
        serializers = self.serializer_class(instance, params, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response({"message": "Profile Updated", "data": serializers.data}, status=status.HTTP_200_OK)
        return Response({"message": "Profile not updated"}, status=status.HTTP_200_OK)
