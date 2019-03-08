from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('HelpArcApp.urls')),
    path('admin/', admin.site.urls),
    path('HelpArcApp/templates', include('django.contrib.auth.urls')),
]
