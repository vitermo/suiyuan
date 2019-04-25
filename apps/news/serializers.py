from rest_framework import serializers
from .models import News,NewsCategory,Comment,Banner
from apps.xfzauth.serializers import UserSerializers

class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')

class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializers()
    author = UserSerializers()
    class Meta:
        model = News
        fields = ('id','title','desc','thumbnail','pub_time','category','author')

class CommentSerializers(serializers.ModelSerializer):
    author = UserSerializers()
    class Meta:
        model = Comment
        fields = ('id','content','author','pub_time')

class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id','image_url','link_to','priority')