from .models import News, User_profile, Likes
from .serializers import NewsListeSrializers
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema, no_body

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class NewsLCView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsListeSrializers


    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_lastest_10_news']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:

            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
            
    
    @action(detail=False, methods=['get'])
    def get_lastest_10_news(self, request):
        news = self.get_queryset().order_by('-time')[:10]
        news_serializer = self.get_serializer(news, many=True)
        return Response(data={"msg":"yangiliklar", "news": news_serializer.data})

    
    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=['post'])
    def user_like(self, request, pk=None):
        news = self.get_object()


        try:
            user = User_profile.objects.get(user=request.user)
        except User_profile.DoesNotExist:
            return Response(
                data={"msg": "Sizning profilingiz topilmadi. Avval profil yarating."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Like yara
        try:
            Likes.objects.create(
                news=news,
                user=user,
            )
            return Response(data={"msg": "Like bosildi"}, status=status.HTTP_201_CREATED)
        
        except Exception:

            return Response(
                data={"msg": "Bu yangilikka oldin like bosilgan"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
            return Response({"msg": "Logout qilindi"}, status=status.HTTP_200_OK)
        return Response({"msg": "Token topilmadi"}, status=status.HTTP_400_BAD_REQUEST)