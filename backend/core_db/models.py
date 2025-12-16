"""
Database models.
"""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a new superuser."""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []



class ReviewPost(models.Model):
    reviewer = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )

    review_title = models.CharField(max_length=150)
    book_title = models.CharField(max_length=255)
    book_author = models.CharField(max_length=150)

    review_image = models.ImageField(
        upload_to='review_images/',
        blank=True,
        null=True,
    )
    review_content = models.TextField()
    genre = models.CharField(max_length=255)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating must be between 1 and 5 stars.'
    )
    review_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    class Meta:
        ordering = ['-review_date']


class Interaction(models.Model):
    reader = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )

    review_post = models.ForeignKey(
        'ReviewPost',
        on_delete=models.CASCADE,
    )
    interaction_type = models.CharField(max_length=255)
