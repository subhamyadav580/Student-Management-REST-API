from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework_social_oauth2.urls')),
    path('api/v1/auth/login/', include('apps.oauth.urls')),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/certificates/', include('apps.certificates.urls')),
    path('api/v1/lectures/', include('apps.lectures.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)