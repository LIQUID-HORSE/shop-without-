from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#отслеживание других url адресов
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reg_log.urls')),
    path('', include('lk.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
