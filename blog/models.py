from django.db import models
from users.models import CustomUser
import uuid
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length = 100)
    author = models.ForeignKey(CustomUser, related_name = 'posts', null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(Category, related_name = 'posts_list')
    body = models.TextField(max_length=1000)
    likes = models.ManyToManyField(CustomUser, related_name='post_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f'{self.title} by {self.author.username}'
    
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, related_name = 'comments', on_delete = models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='post_comments', null=True, on_delete=models.SET_NULL)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        return f"{self.body[:20]} by {self.author.username}"
    
