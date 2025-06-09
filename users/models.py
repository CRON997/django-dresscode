from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.utils.html import strip_tags

class CustomerUser(AbstractUser):
    ...