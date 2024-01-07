from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

def delete_old_profile_image(sender, instance, **kwargs):
    # Delete the old profile image when a new one is uploaded
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    if old_instance.avatar and old_instance.avatar != instance.avatar:
        old_instance.avatar.delete(save=False)

@receiver(pre_save, sender=Profile)
def delete_old_profile_image_pre_save(sender, instance, **kwargs):
    # Connect to the pre_save signal to delete the old profile image
    delete_old_profile_image(sender, instance, **kwargs)

@receiver(post_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    # Delete the profile image when a profile is deleted
    if instance.avatar:
        instance.avatar.delete(save=False)

# Connect to the post_delete signal to delete the profile image when a profile is deleted
post_delete.connect(delete_profile_image, sender=Profile)