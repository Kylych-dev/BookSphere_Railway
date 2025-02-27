from django.db import models
from ..users.models import User
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Абстрактная модель для общих полей (created/updated)
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


class Author(TimeStampedModel):
    first_name = models.CharField(_('first_name'), max_length=100)
    last_name = models.CharField(_('last_name'), max_length=100)
    biography = models.TextField(_('biography'), blank=True)
    date_of_birth = models.DateField(_('date of birth'))
    date_of_death = models.DateField(_('date of death'), null=True, blank=True)


    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Genre(TimeStampedModel):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)


    class Meta:
        ordering = ['name']
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return f'{self.name}'


class Book(TimeStampedModel):
    title = models.CharField(_('title'), max_length=255)
    summary = models.TextField(_('summary'), blank=True)
    isbn = models.CharField(
        _('ISBN'),
        max_length=13,
        unique=True,
        help_text=_('13-character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    )
    genres = models.ManyToManyField(Genre, related_name='books', verbose_name=_('genres'), blank=True)
    authors = models.ManyToManyField(Author, related_name='authored_books', verbose_name=_('authors'), through='BookAuthor')
    publication_date = models.DateField(_('publication date'), db_index=True)


    class Meta:
        ordering = ['-publication_date', 'title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['publication_date']),
        ]
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def __str__(self):
        return self.title

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, related_name='book_authors', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, related_name='author_books', on_delete=models.CASCADE)
    contribution = models.CharField(_('contribution'), max_length=255, blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)


    class Meta:
        ordering = ['order']
        unique_together = ('book', 'author')


class FavoriteBook(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorite_by')


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_favorite_book',
            )
        ]
        verbose_name = _('favorite book')
        verbose_name_plural = _('favorite books')

    def __str__(self):
        return f'{self.user} ❤ {self.book.title}'