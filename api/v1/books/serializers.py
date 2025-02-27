from rest_framework import serializers
from django.db import transaction

from apps.library.models import (
    Book,
    Author,
    Genre,
    FavoriteBook,
    BookAuthor
)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True, read_only=True, source='genre.only')

    author_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.only('id'),
        write_only=True
    )

    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.only('id'),
        source='genres',
        write_only=True
    )

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'summary',
            'isbn',
            'authors',
            'genres',
            'author_ids',
            'genre_ids',
            'publication_date'
        ]
        extra_kwargs = {
            'isbn': {'validators': []},
        }

    def get_authors(self, obj):
        return [
            {
                'id': author.id,
                'name': f'{author.first_name} {author.last_name}'}
            for author in obj.authors.all()

        ]

    def create(self, validated_data):
        author_ids = validated_data.pop('author_ids', [])
        genres = validated_data.pop('genres', [])
        book = Book.objects.create(**validated_data)
        book.genres.set(genres)

        for author in author_ids:
            BookAuthor.objects.create(book=book, author=author)
        return book

    def update(self, instance, validated_data):
        author_ids = validated_data.pop('author_ids', None)
        genres = validated_data.pop('genres', None)
        instance = super().update(instance, validated_data)

        if genres is not None:
            instance.genres.set(genres)

        if author_ids is not None:
            instance.authors.set(author_ids)

        return instance


class FavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = ['user', 'book', 'created_at', 'updated_at']
