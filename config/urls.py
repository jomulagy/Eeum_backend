from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/account/', include("account.urls")),
    path('api/word/', include("word.urls")),
    path('api/message/', include("message.urls")),
    path('api/search/', include("search.urls")),
    path("api/vocabulary/",include("vocabulary.urls")),
    path("api/question/", include("question.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
