from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse
from core.views import force_provision

def api_info(request):
    return JsonResponse({
        'message': 'GRIELISHA API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'products': '/api/products/',
            'services': '/api/services/',
            'orders': '/api/orders/',
            'bookings': '/api/bookings/',
            'docs': '/api/docs/',
            'schema': '/api/schema/',
            'admin': '/admin/'
        }
    })

urlpatterns = [
    path('', api_info, name='api_info'),
    path('api/debug/provision/', force_provision, name='force_provision'),
    path('api/', api_info, name='api_info_alt'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/services/', include('services.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
