from rest_framework import serializers
from .models import *

User = get_user_model()


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'title', 'url', 'private', 'created_at', 'private', 'owner')
        extra_kwargs = {'owner': {'default': serializers.CurrentUserDefault()}}


class BookmarkSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('title', 'url', 'private')


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password", )
