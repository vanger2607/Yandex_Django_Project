from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as mediaserve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("", include("duels.urls")),
    path("", include("users.urls")),
    path("", include("questions.urls")),
    path("errors/", include("errors.urls"))
]
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
urlpatterns += [
    re_path(
        f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
        mediaserve,
        {"document_root": settings.MEDIA_ROOT},
    ),
    re_path(
        f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
        mediaserve,
        {"document_root": settings.STATIC_ROOT},
    ),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
