"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from config.settings import base

# todo https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Sessions
# todo try to do data migrations (DML) while dividing app for a few new apps
# todo https://www.geeksforgeeks.org/software-engineering-coupling-and-cohesion/ ; two scoops of django
# todo check pbkdf2 storage password standard; c
# todo книжка искусство джанго


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls', namespace='home')),
    path('courses/', include('apps.management.urls', namespace='management')),
    path('accounts/', include('apps.authentication.urls', namespace='authentication')),
    path('tinymce/', include('tinymce.urls')),
    path('courses/<int:pk>/tasks/<int:pktask>/', include('apps.assessment.urls', namespace='assessment')),
]

if base.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()
