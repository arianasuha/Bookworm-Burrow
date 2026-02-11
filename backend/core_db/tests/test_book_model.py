from django.test import TestCase
from django.db.utils import IntegrityError
from backend.core_db.models import Book

class BookModelTests(TestCase):
    """Test cases for the Book model."""

    def test_create_book_success(self):
        """Test creating a book is successful and returns string representation."""
        book = Book.objects.create(
            title='The Great Gatsby',
            author='F. Scott Fitzgerald'
        )

        self.assertEqual(str(book), 'The Great Gatsby by F. Scott Fitzgerald')
        self.assertEqual(book.title, 'The Great Gatsby')

    def test_slug_generated_on_save(self):
        """Test that a slug is automatically generated based on title and author."""
        book = Book.objects.create(
            title='The Hobbit',
            author='J.R.R. Tolkien'
        )
        self.assertEqual(book.slug, 'the-hobbit-jrr-tolkien')

    def test_duplicate_slug_appends_counter(self):
        """Test that identical slugs get a counter appended to remain unique."""
        book1 = Book.objects.create(title='Duplicate', author='Author')
        book2 = Book.objects.create(title='Duplicate', author='Author 1')

        self.assertTrue(book2.slug.startswith('duplicate-author'))
        self.assertNotEqual(book1.slug, book2.slug)
        self.assertIn('-1', book2.slug)

    def test_unique_together_constraint(self):
        """Test that same title and author combination raises IntegrityError."""
        Book.objects.create(title='Unique Book', author='Original Author')

        with self.assertRaises(IntegrityError):
            Book.objects.create(title='Unique Book', author='Original Author')

    # why do i need to  give the user access to create a manual slug?