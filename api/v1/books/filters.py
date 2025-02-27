import django_filters
from apps.library.models import Book

class BookFilter(django_filters.FilterSet):
    publication_date__gte = django_filters.DateFilter(
        field_name='publication_date', lookup_expr='gte'
    )
    publication_date__lte = django_filters.DateFilter(
        field_name='publication_date', lookup_expr='lte'
    )
    author_last_name = django_filters.CharFilter(
        field_name='author__last_name', lookup_expr='icontains'
    )

    class Meta:
        model = Book
        fields = {
            'genres': ['exact'],
            'title': ['icontains']
        }