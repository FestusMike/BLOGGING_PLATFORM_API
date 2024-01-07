from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, CommentViewSet, PostViewSet, LikePostAPIView

app_name = 'blog'

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"^comment/(?P<post_id>[0-9a-f-]+)", CommentViewSet, basename='comment')
router.register(r"posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("like/<uuid:pk>/", LikePostAPIView.as_view(), name='like-post'),
]