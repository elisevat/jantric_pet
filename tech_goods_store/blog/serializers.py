import io
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Posts

class PostsModel:
    def __init__(self, title, content):
        self.title = title
        self.content = content


class PostsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()


def encode():
    post = PostsModel(title='Пост drf', content='Первый пост для drf')
    post_sr = PostsSerializer(post)
    print(post_sr, post_sr.data, type(post_sr.data), sep='\n')
    json = JSONRenderer().render(post_sr.data)
    print(json)


def decode():
    stream = io.BytesIO(b'{"title":"\xd0\x9f\xd0\xbe\xd1\x81\xd1\x82 drf","content":"\xd0\x9f\xd0\xb5\xd1\x80\xd0\xb2\xd1\x8b\xd0\xb9 \xd0\xbf\xd0\xbe\xd1\x81\xd1\x82 \xd0\xb4\xd0\xbb\xd1\x8f drf"}')
    data = JSONParser().parse(stream)
    serializer = PostsSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)