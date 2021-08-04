from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )

    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(null=True)
