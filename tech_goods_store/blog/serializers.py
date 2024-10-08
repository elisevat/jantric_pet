import io
from rest_framework import serializers

from .models import Posts



class PostsSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Posts
        fields = ('pk', 'title', 'content', 'image', 'cats', 'author', 'is_published')