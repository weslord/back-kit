from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

#from apps.__SOMEAPP__.urls import SOMEAPP_routes

from apps.user.urls import urlpatterns as user_routes


all_routes = routers.DefaultRouter()
#all_routes.registry.extend(SOMEAPP_routes.registry)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Django REST framework (browsable API)
    path('api-auth/', include('rest_framework.urls')),

    # App routes
    path('api/', include(
        all_routes.urls
        + user_routes
    ))
]
