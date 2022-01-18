from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_staffuser(self, email, password, **extra_fields):
    #     """
    #     Creates and saves a staff user with the given email and password.
    #     """
    #     user = self.create_user(
    #         email,
    #         password=password,
    #         **extra_fields
    #     )
    #     user.is_staff = True
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user





class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_students = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     return self.staff

    # @property
    # def is_admin(self):
    #     "Is the user a admin member?"
    #     return self.admin


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=100)
    bio = models.TextField(default='', blank=True)
    preferred_name = models.CharField(max_length=100, null=True)
    avatar_url = models.CharField(max_length=255, null=True)
    discord_name = models.CharField(max_length=100, null=True)
    github_username = models.CharField(max_length=100)
    codepen_username = models.CharField(max_length=100, null=True)
    fcc_profile_url = models.CharField(max_length=255, null=True)

    LEVELS = (
        (1, 'Level One'),
        (2, 'Level Two'),
    )
    current_level = models.IntegerField(choices=LEVELS, default=1)

    phone = models.CharField(max_length=50, null=True)
    timezone = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.name}'