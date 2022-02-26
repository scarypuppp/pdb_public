from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = [
    path('pro-dj-admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('api/', include('api.urls')),
    path('users/', include('users.urls')),
    path('ajax_select/', include(ajax_select_urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)