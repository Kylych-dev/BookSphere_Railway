from typing import Any
from typing import Type
from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from apps.library.models import Author, FavoriteBook
from api.v1.books.serializers import AuthorSerializer, FavoriteBookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes: list[Type[IsAuthenticated]] = [permissions.IsAuthenticated,]

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет автора из базы данных.

        :param request: Request
        :return: Response
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {'detail': f'Автор {instance.first_name} {instance.last_name} удалён.'},
                status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {'detail': 'Автор уже удалён или не существует.'},
                status=status.HTTP_404_NOT_FOUND)

class FavoriteBookViewSet(viewsets.ModelViewSet):
    queryset = FavoriteBook.objects.all()
    serializer_class = FavoriteBookSerializer
    permission_classes: list[Type[IsAuthenticated]] = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return FavoriteBook.objects.filter(user=self.request.user)

    def clear(self, request: Request) -> Response:
        """
        Удалить все избранные книги для текущего пользователя.

        :param request: Request
        :return: Response
        """
        self.get_queryset().delete()
        return Response(
            {"detail": "All favorite books have been removed."},
            status=status.HTTP_204_NO_CONTENT
        )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Удалить конкретную книгу из избранных для текущего пользователя.

        :param request: Request
        :return: Response
        """
        favorite_book = self.get_object()

        if favorite_book.user != request.user:
            return Response(
                {"detail": "You can only remove books from your own favorites."},
                status=status.HTTP_403_FORBIDDEN
            )
        favorite_book.delete()
        return Response(
            {"detail": "The book has been removed from your favorites."},
            status=status.HTTP_204_NO_CONTENT
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)