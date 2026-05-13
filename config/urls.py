from django.contrib import admin
from django.urls import path,include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework. response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

...

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

class CustomTokenObtainSerializer(TokenObtainPairSerializer):
   @classmethod
   def get_token(cls, user):
      token = super().get_token(user)
      token ["username"] = user.psername
      token["is_admin"] = user.is_staff
      return token

class LogoutView(APIView):
   permission_classes = [IsAuthenticated]

   def post(self, request):
      try:
         refresh = request.data["refresh"]
         token = RefreshToken(refresh)
         token.blacklist()

         return Response(data={"1log out"})
      except Exception as e:
         return Response(data={"msg": "error"})

urlpatterns = [
   path('admin/', admin.site.urls), 
   path('news/', include('news.urls')),
   path('api/auth/logout/', LogoutView.as_view(), name='logout'),
   path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path("api/auth/token/", TokenObtainPairView.as_view()),
   path("api/auth/token/refresh/", TokenRefreshView.as_view()),
   path("api/auth/token/verify/", TokenVerifyView.as_view()),
]