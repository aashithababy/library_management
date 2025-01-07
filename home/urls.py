from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home_page'),
]

import debug_toolbar
# Serve static files in development mode (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Serve media files in development mode (optional, if you're using media files)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
    
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]