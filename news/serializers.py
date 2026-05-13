from rest_framework import serializers
from .models import News




class NewsListeSrializers(serializers.ModelSerializer):
    
    class Meta:
        model = News
        fields = ['id','title','author', 'content','category', 'time', 'views', 'image']
        
class NewsCreateSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = News
        fields = ['title','author', 'content','category', 'image']