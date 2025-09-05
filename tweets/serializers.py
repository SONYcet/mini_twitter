from rest_framework import serializers
from django.utils import timezone
from accounts.serializers import UserPublicSerializer
from .models import Tweet, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    tweet = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at', 'tweet']



class TweetSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id', 'user', 'content', 'image',
            'created_at', 'updated_at',
            'likes_count', 'comments_count', 'is_liked'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Like.objects.filter(user=user, tweet=obj).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
