from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer, UserRegistrationSerializer, UserLoginSerializer, ProfileSerializer
from .models import Profile

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
    
