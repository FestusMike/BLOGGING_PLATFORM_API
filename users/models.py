from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_profile_image_extension, check_alphanum
import uuid


# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4, verbose_name='User Identification Number')
    email = models.EmailField(unique=True, verbose_name='Email Address', null=False)
    first_name = models.CharField(null=True, max_length=100, verbose_name='First Name')
    last_name = models.CharField(null=True, max_length=100, verbose_name='Last Name/Surname')
    username = models.CharField(null=False, blank=False, max_length=50, verbose_name='Username', validators=[check_alphanum])
    date_created = models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

def profile_image_path(instance, filename):
    # Generate file path for the profile image
    return f'profiles/{instance.user.username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(null=True, max_length=100)
    avatar = models.ImageField(blank=True, upload_to=profile_image_path, validators=[validate_profile_image_extension])

    def __str__(self):
        return self.user.email


     



    

