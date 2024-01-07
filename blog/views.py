from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Post, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import CategoryReadSerializer, PostReadSerializer, PostWriteSerializer, CommentReadSerializer, CommentWriteSerializer

# Create your views here.

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
    permission_classes = (AllowAny,)

class PostViewSet(viewsets.ModelViewSet):
    #CRUD Posts    
    queryset = Post.objects.all()

    def get_queryset(self):
        return self.queryset.prefetch_related('comments').order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return PostWriteSerializer
        return PostReadSerializer
    
    def get_permissions(self):
        if self.action in ('create'):
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (AllowAny,)

        return super().get_permissions()
    
class CommentViewSet(viewsets.ModelViewSet):
# CRUD comments for a particular post

    queryset = Comment.objects.all()

    def get_queryset(self):
        res = super().get_queryset()
        post_id = self.kwargs.get('post_id')
        return res.filter(post__id = post_id)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return CommentWriteSerializer
        return CommentReadSerializer
    
    def get_permissions(self):
        if self.action in ('create'):
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = IsAuthorOrReadOnly
        else:
            self.permission_classes = (AllowAny,)

        return super().get_permissions()

class LikePostAPIView(APIView):
    #Like or dislike a post

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, id=pk)
        
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response(status=status.HTTP_200_OK)


