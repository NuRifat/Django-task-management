from django.contrib import admin
from django.urls import path,include
from tasks.views import home
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home),
    path("tasks/",include("tasks.urls")),
    path("users/",include("users.urls")),
] + debug_toolbar_urls()