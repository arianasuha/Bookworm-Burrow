"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

class ModelTests(TestCase):
    """Test models."""

    def error_raise(self, exception_type, *args):
        with self.assertRaises(exception_type):
            get_user_model().objects.create_user(*args)

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'u0NpI@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_normalized_successful(self):
        """Test if the user provided email gets normalized."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_create_user_with_duplicate_email(self):
        """Test creating a user with duplicate email fails."""
        email = 'u0NpI@example.com'
        password = 'testpass123'
        get_user_model().objects.create_user(email, password)
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(email, password)

    def test_create_user_with_no_email(self):
        """Test creating a user with no email fails."""
        self.error_raise(ValueError,'', 'testpass123')

    def test_create_user_with_invalid_email(self):
        """Test creating a user with invalid email fails."""
        email = 'test'
        password = 'testpass123'
        self.error_raise(ValueError, email, password)

    def test_create_superuser_successfully(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'u0NpI@example.com',
            'testpass123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser_with_no_email(self):
        """Test creating a superuser with no email fails."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email='',
                password='testpass123'
            )

    def test_slug_generated_from_name(self):
        """Test slug is generated correctly from first and last name."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='pass',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.slug, 'john-doe')

    def test_slug_collision_resolution(self):
        """Test that duplicate names result in unique slugs (name-1, name-2)."""
        get_user_model().objects.create_user(
            email='user1@example.com', password='pass', first_name='John', last_name='Doe'
        )
        user2 = get_user_model().objects.create_user(
            email='user2@example.com', password='pass', first_name='John', last_name='Doe'
        )
        self.assertEqual(user2.slug, 'john-doe-1')

    def test_slug_generated_from_email(self):
        """Test slug is generated correctly from email."""
        user = get_user_model().objects.create_user(
            email='test@example.com', password='pass'
        )
        self.assertEqual(user.slug, 'test')

    def test_slug_fallback_for_invalid_characters(self):
        """Test fallback to email prefix when name contains only symbols."""
        user = get_user_model().objects.create_user(
            email='star_coder@example.com',
            password='pass',
            first_name='!!!', # slugify returns ""
            last_name='???'   # slugify returns ""
        )

        self.assertEqual(user.slug, 'star_coder')

    def test_superuser_is_staff_and_superuser(self):
        """Test that the superuser created has staff and superuser status."""
        user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_with_no_password_fails(self):
        """Test that creating a superuser without a password raises TypeError."""
        with self.assertRaises(TypeError):
            get_user_model().objects.create_superuser(
                email='admin@example.com',
                password=None
            )

    def test_create_staff_user_successful(self):
        """Test creating a user with staff status is successful."""
        email = 'staff@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            is_staff=True,
        )

        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_new_user_is_not_staff_by_default(self):
        """Test that a default user is created with is_staff=False."""
        user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.assertFalse(user.is_staff)

    def test_slug_does_not_change_on_update(self):
        """Test that updating a user's name does not change their slug."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='pass',
            first_name='John',
            last_name='Doe'
        )
        original_slug = user.slug

        user.first_name = 'Jane'
        user.save()

        self.assertEqual(user.slug, original_slug)
