from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    
     path('', views.index_view, name='index_view'), 
     path('admin/', views.admin_view, name='admin_view'),
          
]

# Serve static and media files during development (when DEBUG is True)
if settings.DEBUG:
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)