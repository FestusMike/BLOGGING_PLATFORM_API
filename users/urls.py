from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users import views

app_name = 'users'

urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view()),
    path("login/", views.UserLoginAPIView.as_view()),
    path("logout/", views.UserLogoutAPIView.as_view()),
    path("user/", views.UserAPIView.as_view()),
    path("profile/", views.UserProfileAPIView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    
    path("google-signup/", views.GoogleAuthRedirect.as_view()),
    path(
        "google/redirect", views.GoogleRedirectURIView.as_view(), name="google-redirect-uri"
    ),
]
