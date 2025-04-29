from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Sentry debug view
def trigger_error(request):
    division_by_zero = 1 / 0

schema_view = get_schema_view(
   openapi.Info(
      title="reconPoint API",
      default_version='v1',
      description="reconPoint: An Automated reconnaissance framework.",
      contact=openapi.Contact(email="security@khulnasoft.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('sentry-debug/', trigger_error),  # Sentry error trigger route

    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('target/', include('targetApp.urls')),
    path('scanEngine/', include('scanEngine.urls')),
    path('scan/', include('startScan.urls')),
    path('recon_note/', include('recon_note.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='base/logout.html'), name='logout'),

    path('api/', include(('api.urls', 'api'))),

    path('media/<path:path>', serve, {'document_root': settings.RECONPOINT_RESULTS}, name='serve_protected_media'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
