from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TweetViewSet, CommentViewSet, LikeViewSet
from rest_framework_nested import routers


router = DefaultRouter()
router.register(r'tweets', TweetViewSet, basename='tweet')
router.register(r'comments', CommentViewSet, basename='comment')



urlpatterns = [
    path("", include(router.urls)),

]
