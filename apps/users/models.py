from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    subscribe_to_notifications = models.BooleanField(
        default=True,
        verbose_name='Подписка на уведомления'
    )

    username = models.CharField('username', max_length=30, unique=True)
    email = models.EmailField('email', unique=True)
    password = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.id} - {self.username}'

    def save(self, *args: tuple, **kwargs: dict) -> None:
        """
        перед сохранением пользователя приводит email к нижнему регистру

        :param args: tuple
        :param kwargs: dict
        :return: None
        """
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'users'
