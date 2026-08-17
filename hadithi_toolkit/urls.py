from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('resources/', include('resources.urls')),
    path('community/', include('community.urls')),
    path('wellness/', include('wellness.urls')),
    path('events/', include('events.urls')),
]

# NOTE: We deliberately do NOT use django.conf.urls.static.static() here.
# That helper checks settings.DEBUG internally and silently returns an
# empty urlpatterns list when DEBUG=False -- so it never actually serves
# media in production, even if you don't wrap it in "if settings.DEBUG".
#
# Since this app intentionally doesn't use S3/R2 and accepts that files
# are ephemeral on Render, we serve media directly via django.views.static.serve
# instead, which has no such DEBUG check.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]