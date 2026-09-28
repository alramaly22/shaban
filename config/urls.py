from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.views.static import serve

from coaching.views import sitemap

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("sitemap.xml", sitemap, name="sitemap"),
    path("", include("coaching.urls")),
]

# Media (Transformation before/after photos) is served this way in every
# environment, not just when DEBUG=True. That's unusual for Django, but
# intentional here: this project commits media/ to the repo (see the
# README's "Updating transformation photos" section) instead of using
# an external storage service, so on Vercel the files are already part
# of the deployed, read-only bundle - they just need a URL that serves
# them. django.views.static.serve is normally discouraged in production
# for performance/security reasons, but for a handful of small images
# on a low-traffic site it's a reasonable, dependency-free trade-off.
urlpatterns += [
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
]
