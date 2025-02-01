from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import FAQViewSet

router = routers.DefaultRouter()
router.register(r'faqs', FAQViewSet)

urlpatterns = [
   path('', include(router.urls))
]
