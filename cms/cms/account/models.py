from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(unique=True)
    pic = models.ImageField(upload_to="account", blank=True)
    bio = models.TextField(blank=True)

    REQUIRED_FIELDS = ('email',)

    def __str__(self):
        return self.username

    # class Meta:
        # db_table = 'auth_user'

# @receiver(post_save, sender = User)
# def create_profile(sender, **kwargs):
#     print("message from signal")
#     print(sender, kwargs)

