from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.auth import views as auth_views
from api.v1.books import views as books_views
from api.v1.authors import views as authors_views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [

        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

        path('register/', auth_views.RegisterView.as_view(), name='register'),
        path('login/', auth_views.LoginView.as_view(), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


        path('authors/', authors_views.AuthorViewSet.as_view(
            {
                'get': 'list',
                'post': 'create'
            }
        ), name='author-list'),

        path('authors/<int:pk>/', authors_views.AuthorViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            }
        ), name='author-detail'),

        path('books/', books_views.BookViewSet.as_view(
            {
                'get': 'list',
                'post': 'create'
            }
        ), name='book-list'),

        path('books/<int:pk>/', books_views.BookViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            }
        ), name='book-detail'),

        path('favorites/', authors_views.FavoriteBookViewSet.as_view(
            {
                'get': 'list',
                'post': 'create'
            }
        ), name='favorite-list'),

        path('favorites/<int:pk>/', authors_views.FavoriteBookViewSet.as_view(
            {
                'get': 'retrieve',
                'delete': 'destroy'
            }
        ), name='favorite-detail'),

        path('favorites/clear/', authors_views.FavoriteBookViewSet.as_view(
            {
                'delete': 'clear'
            }
        ), name='favorites-clear'),

        path('genre/', books_views.GenreViewSet.as_view(
            {
                'get': 'list',
                'post': 'create'
            }
        ), name='genre-list'),

    ]
)




'''
[GET] /authors - список авторов     
[POST] /authors - создание автора   
[GET] /authors/{id} - детали автора 
[PUT] /authors/{id} - обновление автора 
[DELETE] /authors/{id} - удаление автора

[GET] /books - список книг с фильтрацией
[POST] /books - создание книги
[GET] /books/{id} - детали книги
[PUT] /books/{id} - обновление книги
[DELETE] /books/{id} - удаление книги

[GET] /favorites - список избранного
[POST] /favorites - добавить в избранное
[DELETE] /favorites/{id} - удалить из избранного
[DELETE] /favorites/clear - очистить избранное

[POST] /register - регистрация
[POST] /login - авторизация
[POST] /logout - выход
[POST] /token/refresh - обновление JWT-токена

'''