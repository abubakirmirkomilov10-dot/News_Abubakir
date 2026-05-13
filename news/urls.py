from django.urls import path, include
from news.views import NewsLCView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('news', NewsLCView, basename='news')

urlpatterns = [
    path('', include(router.urls))
]