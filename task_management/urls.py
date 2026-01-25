from django.contrib import admin
from django.urls import path,include
from core.views import home, no_permission
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("tasks/",include("tasks.urls")),
    path("users/",include("users.urls")),
    path('', home, name="home"),
    path('no-permission/', no_permission, name='no-permission')
] + debug_toolbar_urls()