from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("account.urls")),
    path('word/', include("word.urls")),
    path('message/', include("message.urls")),
    path('search/', include("search.urls")),
    path("vocabulary/",include("vocabulary.urls")),
    path("question/", include("question.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
