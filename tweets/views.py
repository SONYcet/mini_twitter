from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Tweet, Comment, Like
from .serializers import TweetSerializer, CommentSerializer
from accounts.serializers import UserPublicSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().select_related("user").prefetch_related("likes", "comments")
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        tweet = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        if not created:
            return Response({'detail': 'Already liked.'}, status=200)
        return Response({'detail': 'Liked.'}, status=201)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        tweet = self.get_object()
        Like.objects.filter(user=request.user, tweet=tweet).delete()
        return Response({'detail': 'Unliked.'}, status=200)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        tweet = self.get_object()
        qs = tweet.likes.select_related("user").all()
        serializer = UserPublicSerializer([like.user for like in qs], many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        tweet = Tweet.objects.get(id=pk)
        qs = tweet.comments.select_related("user").all()
        serializer = CommentSerializer(qs, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("user", "tweet")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        tweet_id = self.request.data.get("tweet_id")
        if not tweet_id:
            raise serializers.ValidationError({"tweet_id": "This field is required."})

        tweet = Tweet.objects.get(id=tweet_id)
        serializer.save(user=self.request.user, tweet=tweet)


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all().select_related("user", "tweet")
    serializer_class = UserPublicSerializer  # shows who liked the tweet
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        return Response({'detail': 'Use /tweets/{id}/likes/ instead.'})
