from django.test import TestCase
from django.db.utils import IntegrityError
from backend.core_db.models import Genre

class GenreModelTests(TestCase):
    """Test suite for the Genre model."""

    @classmethod
    def setUpTestData(cls):
        """Create the 'System Genres' that would normally exist in Admin."""
        cls.base_genres = ["History", "Horror", "Fiction", "Sci-Fi"]
        for name in cls.base_genres:
            Genre.objects.create(name=name, is_approved=True)

    def test_base_genres_exist(self):
        """Test that the setup genres are created and approved."""
        count = Genre.objects.filter(is_approved=True).count()
        self.assertEqual(count, len(self.base_genres))

    def test_genre_normalization_and_slug(self):
        """Test name is stripped, titled, and slugified automatically."""
        genre = Genre.objects.create(name="  science fiction  ")

        self.assertEqual(genre.name, "Science Fiction")
        self.assertEqual(genre.slug, "science-fiction")

    def test_duplicate_genre_name_fails(self):
        """Test that unique constraint prevents duplicate genre names."""
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name="History")

    def test_suggested_genre_status(self):
        """Test that new genres are pending (is_approved=False) by default."""
        new_suggestion = Genre.objects.create(name="Cyberpunk")

        self.assertFalse(new_suggestion.is_approved)
        self.assertIn("(Pending)", str(new_suggestion))

    def test_approved_genre_string_representation(self):
        """Test that approved genres don't show the (Pending) suffix."""
        genre = Genre.objects.get(name="History")
        self.assertEqual(str(genre), "History")