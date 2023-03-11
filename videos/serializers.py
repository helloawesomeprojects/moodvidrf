from rest_framework import serializers
from .models import Video, Like, Comment, Save
from rest_framework.fields import CurrentUserDefault


class VideoSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Video
        fields = ['id', 'user', 'title', 'description', 'file', 'latitude', 'longitude', 'created_at', 'updated_at',
                  'distance', 'user_detail', 'is_liked', 'is_saved', 'likes_amount', 'saves_amount', 'comments_amount']

    def get_user_detail(self, obj):
        return obj.user_detail

    def get_likes_amout(self, obj):
        return obj.likes_amount

    def get_saves_amout(self, obj):
        return obj.saves_amount

    def get_comments_amount(self, obj):
        return obj.comments_amount

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ['user', 'video']


class SaveSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Save
        fields = ['user', 'video']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'user', 'video','user_detail']

    def get_user_detail(self, obj):
        return obj.user_detail


