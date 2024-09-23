import io
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Posts


class PostsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    content = serializers.CharField(allow_blank=True)
    author_id = serializers.IntegerField()
    date_create = serializers.DateTimeField(read_only=True)
    date_update = serializers.DateTimeField(read_only=True)
    date_publish = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=Posts.Status.DRAFT)
    cats_id = serializers.IntegerField()

    def create(self, validated_data):
        return Posts.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.author_id = validated_data.get("author_id", instance.author_id)
        instance.date_update = validated_data.get("date_update", instance.date_update)
        instance.date_publish = validated_data.get("date_publish", instance.date_publish)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.cats_id = validated_data.get("cats_id", instance.cats_id)
        return instance

