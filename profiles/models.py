from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    image = ImageField(upload_to="profiles",default="1")
    name = models.CharField(max_length=50)
    tagline = models.CharField(max_length=100)
    cover = ImageField(upload_to="profiles", default="1")

    def __str__(self):
        return (self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if (created):
        Profile.objects.create(user=instance)