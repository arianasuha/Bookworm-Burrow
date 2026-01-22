"""
Tests for models.
"""
from django.test import TestCase
from backend.core_db.models import Genre
from django.db import IntegrityError

class ModelTests(TestCase):
    """Test models."""

    def test_str_representation(self):
        """Test the string representation returns the name."""
        genre = Genre.objects.create(name='Fantasy')
        self.assertEqual(str(genre), 'Fantasy')

    def test_name_normalization_to_title(self):
        """Test that the name is always converted to Title Case on save."""
        sample_names = [
            ['science fiction', 'Science Fiction'],
            ['ROMANCE', 'Romance'],
            ['fAnTaSy', 'Fantasy'],
        ]
        for input_name, expected_name in sample_names:
            genre = Genre.objects.create(name=input_name)
            self.assertEqual(genre.name, expected_name)
            genre.delete()

    def test_automatic_slug_generation(self):
        """Test that a slug is generated automatically if not provided."""
        genre = Genre.objects.create(name='Historical Fiction')
        self.assertEqual(genre.slug, 'historical-fiction')

    def test_manual_slug_override(self):
        """Test that providing a custom slug is respected."""
        genre = Genre.objects.create(name='Science Fiction', slug='sci-fi')
        self.assertEqual(genre.slug, 'sci-fi')

    def test_duplicate_name_fails(self):
        """Test that creating a genre with a duplicate name raises an error."""
        Genre.objects.create(name='Action')
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name='Action')

    def test_duplicate_slug_fails(self):
        """Test that different names resulting in the same slug fails (no collision loop)."""
        Genre.objects.create(name='Action')
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name='Action!', slug='')

    def test_ordering(self):
        """Test that genres are ordered alphabetically by name."""
        Genre.objects.create(name='Thriller')
        Genre.objects.create(name='Action')
        Genre.objects.create(name='Horror')

        genres = Genre.objects.all()
        self.assertEqual(genres[0].name, 'Action')
        self.assertEqual(genres[1].name, 'Horror')
        self.assertEqual(genres[2].name, 'Thriller')

    def test_slug_updates_on_name_change(self):
        """Test that the slug updates automatically when the name is changed."""
        genre = Genre.objects.create(name='Old Category')
        self.assertEqual(genre.slug, 'old-category')

        genre.name = 'New Category'
        genre.save()

        self.assertEqual(genre.slug, 'new-category')