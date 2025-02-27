from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.library.models import Author
from rest_framework.reverse import reverse


class AuthorViewSetTest(APITestCase):

    def setUp(self):
        """Создание пользователя и авторов для тестов."""
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Создаем авторов
        self.author_1 = Author.objects.create(
            first_name="John", last_name="Doe", biography="Bio 1", date_of_birth="1970-01-01"
        )
        self.author_2 = Author.objects.create(
            first_name="Jane", last_name="Smith", biography="Bio 2", date_of_birth="1980-01-01"
        )

    def test_get_authors(self):
        """Тестируем получение списка авторов."""
        url = reverse('author-list')  # URL для AuthorViewSet
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Должно быть два автора
        self.assertEqual(response.data[0]['first_name'], self.author_1.first_name)
        self.assertEqual(response.data[1]['first_name'], self.author_2.first_name)

    def test_create_author(self):
        """Тестируем создание нового автора."""
        url = reverse('author-list')
        data = {
            'first_name': 'Alice',
            'last_name': 'Williams',
            'biography': 'Famous author',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Alice')
        self.assertEqual(response.data['last_name'], 'Williams')

    def test_update_author(self):
        """Тестируем обновление данных автора."""
        url = reverse('author-detail', args=[self.author_1.id])  # URL для детальной информации об авторе
        data = {'first_name': 'Updated Name'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated Name')

    def test_delete_author(self):
        """Тестируем удаление автора."""
        url = reverse('author-detail', args=[self.author_1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['detail'], 'Автор John Doe удалён.')

        # Проверим, что автор действительно удален
        author_exists = Author.objects.filter(id=self.author_1.id).exists()
        self.assertFalse(author_exists)

    def test_delete_non_existent_author(self):
        """Тестируем удаление несуществующего автора."""
        url = reverse('author-detail', args=[999])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Автор уже удалён или не существует.')
