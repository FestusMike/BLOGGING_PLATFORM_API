from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.base import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer, UserRegistrationSerializer, UserLoginSerializer, ProfileSerializer
from .models import Profile
import requests

# Create your views here.
User = get_user_model()

class UserRegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)

class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer =self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = RefreshToken.for_user(user)
        response_body = {"refresh": str(token),
                          "access": str(token.access_token)}
        return Response(response_body, status=status.HTTP_200_OK)

class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            response_body = {
                "message" : "User logged out successfully",
                'status' : status.HTTP_205_RESET_CONTENT,
            }
            return Response(response_body)
        except Exception as e:
            response_body = {
                "message": f"Request cannot be processed because {e}",
                'status': status.HTTP_400_BAD_REQUEST,
            }
            return Response(response_body, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

class UserProfileAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile

class GoogleAuthRedirect(View):
    permission_classes = [AllowAny]

    def get(self, request):
        redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&access_type=offline&redirect_uri=http://127.0.0.1:8000/api/google/redirect"
        return redirect(redirect_url)

class GoogleRedirectURIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')
        if code:
            token_endpoint = 'https://oauth2.googleapis.com/token'
            token_params = {
                'code': code,
                'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                'redirect_uri': 'http://127.0.0.1:8000/api/google/redirect',
                'grant_type': 'authorization_code'
            }
            response = requests.post(token_endpoint, data=token_params)
            if response.status_code == 200:
                access_token = response.json().get("access_token")
                if access_token:
                    profile_endpoint = "https://www.googleapis.com/oauth2/v1/userinfo"
                    headers = {'Authorization': f"Bearer {access_token}"}
                    profile_response = requests.get(profile_endpoint, headers=headers)
                    if profile_response.status_code == 200:
                        data = {}
                        profile_data = profile_response.json()
                        email = profile_data["email"]
                        existing_user = User.objects.filter(email=email)
                        if existing_user:
                            error_msg = {"message": "This account already exists"}
                            return Response(error_msg, status.HTTP_400_BAD_REQUEST)
                        user = User.objects.create_user(username=profile_data["given_name"], email=profile_data["email"])
                        if "family_name" in profile_data:
                            user.last_name = profile_data["family_name"]
                            user.save()                        
                        refresh = RefreshToken.for_user(user)
                        data["access_token"] = str(refresh.access_token)
                        data["refresh_token"] = str(refresh)
                        return Response(data, status.HTTP_201_CREATED)
            return Response({}, status.HTTP_400_BAD_REQUEST)
