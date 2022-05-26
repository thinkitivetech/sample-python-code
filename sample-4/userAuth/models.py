from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Custom Model Manager to use email as identifier (username is default identifier)
class UserManager(BaseUserManager):

    def create_superuser(self, email,password, **extra_fields):
            if not email:
                raise ValueError("User must have an email")
            if not password:
                raise ValueError("User must have a password")

            user = self.model(
                email=self.normalize_email(email)
            )
            user.set_password(password) 
            user.is_superuser = True 
            user.is_staff = True 
            user.is_active = True 
            user.save(using=self._db)
            return user

    def create_user(self, email,password,is_admin=False, is_staff=False, is_active=True, **extra_fields):
            if not email:
                raise ValueError("User must have an email")
            if not password:
                raise ValueError("User must have a password")

            user = self.model(
                email=self.normalize_email(email)
            )
           
            user.set_password(password)
            user.admin = is_admin
            user.staff = is_staff
            user.active = is_active
            user.save(using=self._db)
            return user

# Custom user model using AbstractUser as base class
class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True, null=True)
    date_of_birth = models.DateField(null=True)
    age = models.IntegerField(null=True)
    phone_number = models.BigIntegerField(unique=True, null=True)
    address = models.CharField(max_length= 200, null=True)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []