# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers.token import CustomTokenObtainPairSerializer
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except (KeyError, TokenError, InvalidToken):
            return Response({"error": "Invalid or missing refresh token"}, status=status.HTTP_400_BAD_REQUEST)