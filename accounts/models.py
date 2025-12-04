from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    """Class to manage the creation of user objects"""
    
    def make_random_password(self, length=16):
        """Generates a random password of given length using allowed characters"""
        # define the allowed characters including all leters, digits, and some special characters
        allowed_chars = (
            'abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789'
            '!@#$%^&*()-_=+[]{}|;:,.<>?'
        )
        # use random.choice to select characters from the allowed set and join them to form a password of the specified length
        import random
        return ''.join(random.choice(allowed_chars) for _ in range(length))
        
    def get_queryset(self):
        """Returns the queryset of users"""
        return super().get_queryset().filter(is_active=True)

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a user object
        Arguments:
        email: the string to use as email
        password: the string to use as password

        Optionals:
        Any additional fields to set on the User model

        Return:
            A user object
        """

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates an admin user object
        Arguments:
        username: the string to use as username
        email: the string to use as email
        password: the string to use as password

        Return:
            A user object
        """
        user = self.create_user(email, password=password)
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    username = models.CharField(max_length=25, unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name='Email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        
    def __str__(self):
        return self.username or self.email

    def disable(self, using=None, keep_parents=False):
        self.is_active ^= True
        self.save()

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_name(self):
        if self.get_profile():
            return f"{self.get_profile().identifier} - {self.get_full_name()}"
        return self.get_full_name()
    
    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_initials(self):
        """Returns the initials of the user"""
        initials = ""
        if self.first_name:
            initials += self.first_name[0].upper()
        if self.last_name:
            initials += self.last_name[0].upper()
        if not initials and self.username:
            initials = self.username[:1].upper()
        if not initials and self.email:
            initials = self.email[:1].upper()
        return initials

    def get_profile(self):
        """Returns the user profile"""
        try:
            return self.profile
        except Exception:
            return None
    
    def get_identifier(self):
        profile = self.get_profile()
        return profile.identifier if profile and profile.identifier else "N/A"
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class UserProfile(models.Model):
    class Genders(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="profile")

    identifier = models.CharField(_("Unique Identifier"), max_length=20, unique=True, null=True, blank=True)
    
    gender = models.CharField(_("Gender"), max_length=1, choices=Genders.choices, default=Genders.FEMALE)
    phone_1 = models.CharField(_("Phone (Main)"), max_length=20, null=True, blank=True)
    phone_2 = models.CharField(_("Phone (Other)"), max_length=20, null=True, blank=True)
    
    