from django.contrib import admin

from .models import (
    Author,
    Book,
    Genre,
    BookAuthor,
    FavoriteBook
)


class AuthorAdmin(admin.ModelAdmin):
    """
    Авторы с расширенным поиском
    """
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    search_fields = ('last_name', 'first_name')
    list_filter = ('date_of_birth',)
    fields = (('first_name', 'last_name'), ('date_of_birth', 'date_of_death'), 'biography')
    readonly_fields = ('created_at', 'updated_at')


class GenreAdmin(admin.ModelAdmin):
    """
    Жанры с описанием
    """
    list_display = ('name', 'description_short')
    search_fields = ('name',)

    def description_short(self, obj):
        return f"{obj.description[:50]}..." if obj.description else ""

    description_short.short_description = "Description"


class BookAuthorInline(admin.TabularInline):
    """
    Inline для авторов книги
    """
    model = BookAuthor
    extra = 1
    autocomplete_fields = ['author']


class BookAdmin(admin.ModelAdmin):
    """
    Админка для книг с расширенными возможностями
    """
    list_display = ('title', 'publication_date', 'isbn_short', 'author_list', 'genre_list')
    list_filter = ('genres', 'publication_date')
    search_fields = ('title', 'isbn', 'authors__last_name')
    filter_horizontal = ('genres',)
    inlines = [BookAuthorInline]
    # readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'isbn')
        }),
        ('Content', {
            'fields': ('summary', 'genres')
        }),
        ('Publication', {
            'fields': ('publication_date',)
        })
    )

    def isbn_short(self, obj):
        return f"{obj.isbn[:5]}..." if obj.isbn else ""

    isbn_short.short_description = "ISBN"

    def author_list(self, obj):
        return ", ".join([str(author) for author in obj.authors.all()])

    author_list.short_description = "Authors"

    def genre_list(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    genre_list.short_description = "Genres"


class FavoriteBookAdmin(admin.ModelAdmin):
    """
    Избранные книги
    """
    list_display = ('user', 'book', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'book__title')
    autocomplete_fields = ['user', 'book']
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(FavoriteBook, FavoriteBookAdmin)