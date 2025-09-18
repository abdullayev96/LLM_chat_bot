from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("llm.urls")),
    path("", include("django_prometheus.urls")),
]





#####  admin
###   12345 .....