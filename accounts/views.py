from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from accounts.models import Profile, Follow
from accounts.permissions import IsSelfOrReadOnly
from accounts.serializers import RegisterSerializer, ProfileSerializer, UserPublicSerializer


# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [IsSelfOrReadOnly]


def perform_update(self, serializer):
    serializer.save(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        u = request.user
        followers_count = Follow.objects.filter(following=u).count()
        following_count = Follow.objects.filter(follower=u).count()
        data = UserPublicSerializer(u).data
        data.update({
            'followers_count': followers_count,
            'following_count': following_count
        })
        return Response(data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        target = self.get_object()
        if target == request.user:
            return Response({'detail': "You can't follow yourself."}, status=400)
        obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            return Response({'detail': 'Already following.'}, status=200)
        return Response({'detail': 'Followed.'}, status=201)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        target = self.get_object()
        Follow.objects.filter(follower=request.user, following=target).delete()
        return Response({'detail': 'Unfollowed.'}, status=200)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        qs = user.followers.select_related('follower').all()
        data = [{'id': f.follower.id, 'username': f.follower.username} for f in qs]
        return Response({'count': len(data), 'results': data})

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        qs = user.following.select_related('following').all()
        data = [{'id': f.following.id, 'username': f.following.username} for f in qs]
        return Response({'count': len(data), 'results': data})