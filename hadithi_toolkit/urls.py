from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from core.views import debug_media
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('resources/', include('resources.urls')),
    path('community/', include('community.urls')),
    path('wellness/', include('wellness.urls')),
    path('events/', include('events.urls')),
    path('debug-media/', debug_media),
]

# Serve media files unconditionally (not just when DEBUG=True).
# This is needed because Render's filesystem is ephemeral and this
# app intentionally isn't using S3/R2 — files are only expected to
# be downloadable until the next redeploy/restart.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)