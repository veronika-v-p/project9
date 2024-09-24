from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Настройка схемы для Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Биржа материалов API",
      default_version='v1',
      description="Документация для API биржи материалов",
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    # Админ панель
    path('admin/', admin.site.urls),
    
    # Подключение приложения main
    path('', include('main.urls')),
    
    # Swagger документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    
]