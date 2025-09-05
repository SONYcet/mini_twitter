from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import Profile, Follow


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        password= validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    class Meta:
        model=Profile
        fields=['id', 'user','bio', 'avatar', 'created_at']

class FollowSerializer(serializers.ModelSerializer):
    follower = UserPublicSerializer(read_only=True)
    following = UserPublicSerializer(read_only=True)
    class Meta:
        model=Follow
        fields=['id', 'follower','following', 'created_at']
