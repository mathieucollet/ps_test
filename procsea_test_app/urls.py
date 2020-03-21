from django.urls import path, include
from rest_framework import routers

from test_app import views

router = routers.DefaultRouter()
router.register(r'', views.RegionViewSet, basename='region-list')

urlpatterns = [
    path('', include(router.urls))
]
