from typing import List

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.books.serializers import BookSerializer, GenreSerializer
from apps.library.models import Book, Genre
from .filters import BookFilter


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления книгами.

    Поддерживает операции CRUD (создание, получение, обновление, удаление)
    с возможностью фильтрации, поиска и сортировки.
    """
    queryset = Book.objects.prefetch_related('authors')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'authors__last_name']
    ordering_fields = ['publication_date', 'authors__last_name', 'genres__name']
    ordering = ['-publication_date',]

    def get_permissions(self) -> List[permissions.BasePermission]:
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления жанрами книг.

    Поддерживает стандартные CRUD-операции.
    Доступ к данным разрешён только аутентифицированным пользователям.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated,]

