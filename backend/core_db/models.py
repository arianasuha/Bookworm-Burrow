"""
Database models.
"""
from django.db import models
from django.utils.text import slugify
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
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # if creating a new user (self.pk is None) AND the slug is empty
        if not self.pk and not self.slug:

            f_name = self.first_name if self.first_name else ''
            l_name = self.last_name if self.last_name else ''

            if f_name or l_name:
                 full_name = f'{f_name} {l_name}'
            else:
                 full_name = self.email.split('@')[0]

            base_slug = slugify(full_name)

            # Check for empty slug (if email part was only illegal characters)
            if not base_slug:
                # Use the primary key to ensure a unique slug is always created
                base_slug = f"user-{self.email.split('@')[0]}"

            # 4. Collision-checking loop for uniqueness
            new_slug = base_slug
            counter = 1

            while self.__class__.objects.filter(slug=new_slug).exists():
                new_slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = new_slug

        super().save(*args, **kwargs)

    def __str__(self):
        """String representation of the user object."""
        return self.email


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f'{self.title} {self.author}')

            # Collision-checking loop
            new_slug = base_slug
            counter = 1

            while Book.objects.filter(slug=new_slug).exists():
                new_slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} by {self.author}'

    class Meta:
        unique_together = ('title', 'author')


class ReviewPost(models.Model):
    reviewer = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )

    review_title = models.CharField(max_length=150)
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    reviewer_genres = models.ManyToManyField(
        'Genre',
        related_name='reviews_by_opinion',
        blank=True,
    )
    review_image = models.ImageField(
        upload_to='review_images/',
        blank=True,
        null=True,
    )
    review_content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating must be between 1 and 5 stars.'
    )
    review_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.review_title)
            unique_slug_base = f'{base_slug}-by-{self.reviewer.slug}'

            counter = 1
            final_slug = unique_slug_base
            while ReviewPost.objects.filter(slug=final_slug).exists():
                final_slug = f'{unique_slug_base}-{counter}'
                counter += 1

            self.slug = final_slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-review_date']



class Interaction(models.Model):

    class InteractionTypes(models.TextChoices):
        LOVE = 'LOVE', 'Love'
        LIKE = 'LIKE', 'Like'
        COMMENT = 'COMMENT', 'Comment'

    reader = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='interactions_given',
    )

    review_post = models.ForeignKey(
        'ReviewPost',
        on_delete=models.CASCADE,
        related_name='interactions',
    )

    interaction_type = models.CharField(
        max_length=7,
        choices=InteractionTypes.choices,
    )


    content = models.TextField(
        blank=True,
        null=True,
        help_text='Only required if the interaction type is COMMENT.'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f'{self.reader} {self.interaction_type}d on "{self.review_post.review_title}"'