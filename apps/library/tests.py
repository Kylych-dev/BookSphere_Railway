from django.test import TestCase
from django.utils import timezone
from .models import Author


class AuthorModelTest(TestCase):

    def setUp(self):
        """Создание тестового автора для тестов."""
        self.author = Author.objects.create(
            first_name="John",
            last_name="Doe",
            biography="A famous writer.",
            date_of_birth="1970-01-01",
            date_of_death=None
        )

    def test_author_creation(self):
        """Тестирование создания автора."""
        author = self.author
        self.assertEqual(author.first_name, "John")
        self.assertEqual(author.last_name, "Doe")
        self.assertEqual(author.biography, "A famous writer.")
        self.assertEqual(str(author.date_of_birth), "1970-01-01")
        self.assertIsNone(author.date_of_death)


    def test_author_ordering(self):
        """Тестирование порядка сортировки авторов по фамилии и имени."""
        author1 = Author.objects.create(
            first_name="Jane",
            last_name="Doe",
            biography="Another famous writer.",
            date_of_birth="1980-01-01",
            date_of_death=None
        )

        author2 = Author.objects.create(
            first_name="Alice",
            last_name="Smith",
            biography="A different writer.",
            date_of_birth="1990-01-01",
            date_of_death=None
        )

        authors = Author.objects.all()
        self.assertEqual(authors[0], author2)
        self.assertEqual(authors[1], author1)
        self.assertEqual(authors[2], self.author)

