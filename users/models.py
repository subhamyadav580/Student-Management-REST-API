import os
from email.policy import default
from statistics import mode
from django.conf import settings
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
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


class UserProfile(models.Model):
    email = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    fname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    bio = models.TextField(default='', blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    contact_add = models.TextField(default="", blank=True)
    gender_choices = (
        (0, 'Select Gender'),
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Transgender')
    )
    gender = models.IntegerField(choices=gender_choices, default=0)
    age = models.IntegerField()
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        return f"{self.fname} {self.mname} {self.lname}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance=None, created=False, **kwargs,):
	if created:
		UserProfile.objects.create(email=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs,):
	if created:
            Token.objects.create(user=instance)

@receiver(pre_save, sender=UserProfile)
def pre_save_image(sender, instance, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = sender.objects.get(email=instance).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


@receiver(post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
