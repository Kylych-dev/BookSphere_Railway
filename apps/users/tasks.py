from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import User
from ..library.models import Book
from datetime import timedelta
from core.settings import EMAIL_HOST_USER


@shared_task
def send_daily_new_books():
    """Отправка списка новых книг за последние 24 часа"""
    yesterday = timezone.now() - timedelta(days=1)
    new_books = Book.objects.filter(created_at__gte=yesterday)

    if new_books.exists():
        for user in User.objects.filter(subscribe_to_notifications=True):
            subject = 'Новые книги за последние 24 часа'
            message = '\n'.join([f'- {book.title}' for book in new_books])
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                ['mirbekov1kylych@gmail.com'],
                fail_silently=False
            )

@shared_task
def check_anniversary_books():
    """Проверка юбилейных дат публикации"""
    today = timezone.now().date()
    anniversary_years = [5, 10, 20]

    for year in anniversary_years:
        target_year = today.year - year
        try:
            target_date = today.replace(year=target_year)
        except ValueError:
            target_date = today.replace(year=target_year, day=today.day - 1)

        anniversary_books = Book.objects.filter(publication_date=target_date)

        if anniversary_books.exists():
            for user in User.objects.filter(subscribe_to_notifications=True):
                subject = f'Юбилейные книги ({year} лет)'
                message = '\n'.join([f'- {book.title}' for book in anniversary_books])

                send_mail(
                    subject,
                    message,
                    EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )

