from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
      title="Books API",
      default_version='v1',
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.v1.router')),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
