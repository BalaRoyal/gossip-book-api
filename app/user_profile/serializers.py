from rest_framework import serializers
from taggit.models import Tag

from .models import Followers, User, UserLocation


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class FollowersSerializer(serializers.ModelSerializer):
    """
    Convert user followers table model to and Form JSON
    """
    class Meta:
        model = Followers
        fields = '__all__'

        read_only_fields = ('created_at', 'updated_at',
                            'follower', 'user', 'following')


class UserLocationSerializer(serializers.ModelSerializer):
    """ Serializes user location model object to and from JSON """

    class Meta:

        model = UserLocation
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    """
    Converts user model object to and from JSON.
    """

    address = UserLocationSerializer(many=True, read_only=True)
    followers = FollowersSerializer(many=True, read_only=True)
    following = FollowersSerializer(many=True, read_only=True)
    interested_topics = TagSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name', 'middle_name',
            'last_name', 'email',
            'username', 'title',
            'bio',
            'password',
            'created_at',
            'updated_at',
            'address',
            'is_active',
            'followers',
            'following',
            'interested_topics',
            'profile_image_url'
        )

        read_only_fields = ('id', 'created_at', 'updated_at', 'is_active')

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def update(self, instance, validated_data):
        """ Override the update instance serializer method to hash passwords."""

        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)

            else:
                setattr(instance, attr, value)

        instance.save()

        return instance

    def create(self, validated_data):
        password = validated_data.pop('password')

        if password:
            instance = User.objects.create(**validated_data)

            instance.set_password(password)
            instance.is_active = False
            instance.save()

            return instance
        else:
            raise ValueError('Password is required')
