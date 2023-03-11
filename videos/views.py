from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from haversine import haversine
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Video, Like, Comment, Save
from .serializers import VideoSerializer, CommentSerializer, SaveSerializer, LikeSerializer
from rest_framework import status


class RecommendationApiView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        queryset = self.get_queryset()
        pk = 0
        if request.user.is_authenticated:
            pk = request.user.pk
        user_location = (
            float(request.query_params.get('lat', 12.12)), float(request.query_params.get('lon', 23.455)))
        for obj in queryset:
            video_location = (float(obj.latitude), float(obj.longitude))
            obj.distance = haversine(user_location, video_location)
            likes = Like.objects.filter(user=pk, video=obj)
            obj.is_liked = likes.count()
            saves = Save.objects.filter(user=pk, video=obj)
            obj.is_saved = saves.count()
        queryset = sorted(queryset, key=lambda x: x.distance)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VideoApiView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = self.get_queryset()
        pk = request.user.pk
        for obj in queryset:
            obj.is_liked = pk
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class LikeApiView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        user = request.user
        pk = request.data.get('video')
        try:
            obj = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        status_action = "No changes"
        like = Like.objects.filter(user=user, video=obj)
        if like.count() > 0:
            like.delete()
            status_action = "like deleted"

        else:
            like = Like.objects.create(user=user, video=obj)
            status_action = "Like created"
        save = Save.objects.filter(user=user, video=obj)
        like = Like.objects.filter(user=user, video=obj)
        obj.is_saved = save.count()
        obj.is_liked = like.count()
        serializer = VideoSerializer(obj)
        return Response({"status": status_action, "video": serializer.data})


class SaveApiView(generics.ListCreateAPIView):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        pk = request.data.get('video')
        try:
            obj = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        status_action = "No changes"
        save = Save.objects.filter(user=user, video=obj)
        if save.count() > 0:
            save.delete()
            status_action = "save deleted"

        else:
            save = Save.objects.create(user=user, video=obj)
            status_action = "Save created"
        save = Save.objects.filter(user=user, video=obj)
        like = Like.objects.filter(user=user, video=obj)
        obj.is_saved = save.count()
        obj.is_liked = like.count()
        serializer = VideoSerializer(obj)
        return Response({"status": status_action, "video": serializer.data})


class CommentApiView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        pk = request.data.get('video')
        try:
            obj = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.create(user=user, video=obj, comment=request.data.get('comment'))
        save = Save.objects.filter(user=user, video=obj)
        like = Like.objects.filter(user=user, video=obj)
        obj.is_saved = save.count()
        obj.is_liked = like.count()
        serializer = VideoSerializer(comment.video)
        serializer_2=CommentSerializer(comment)
        return Response({"status": "comment created", "comment": serializer_2.data, "video": serializer.data})

class Userdata(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        return Response({"name": user.username,
                "email": user.email})

class UserVideo(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        videos = Video.objects.filter(user=user,)
        for obj in videos:
            likes = Like.objects.filter(user=user, video=obj)
            obj.is_liked = likes.count()
            saves = Save.objects.filter(user=user, video=obj)
            obj.is_saved = saves.count()
        serializer = self.get_serializer(videos, many=True)
        return Response({"videos": serializer.data})

class UserLikedVideo(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        likes = Like.objects.filter(user=user).prefetch_related('video')
        videos = [like.video for like in likes]
        for obj in videos:
            likes = Like.objects.filter(user=user, video=obj)
            obj.is_liked = likes.count()
            saves = Save.objects.filter(user=user, video=obj)
            obj.is_saved = saves.count()
        serializer = self.get_serializer(videos, many=True)
        return Response({"videos": serializer.data})

class UserSavedVideo(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        saves = Save.objects.filter(user=user).prefetch_related('video')
        videos = [save.video for save in saves]
        for obj in videos:
            likes = Like.objects.filter(user=user, video=obj)
            obj.is_liked = likes.count()
            saves = Save.objects.filter(user=user, video=obj)
            obj.is_saved = saves.count()
        serializer = self.get_serializer(videos, many=True)
        return Response({"videos": serializer.data})


class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        pk = 0
        if request.user.is_authenticated:
            pk = request.user.pk

        user_location = (float(request.query_params.get('lat', 12.12)), float(request.query_params.get('lon', 23.455)))

        # Get all videos except the video with the specific id
        queryset = Video.objects.exclude(id=instance.id)
        for obj in queryset:
            video_location = (float(obj.latitude), float(obj.longitude))
            obj.distance = haversine(user_location, video_location)
            likes = Like.objects.filter(user=pk, video=obj)
            obj.is_liked = likes.count()
            saves = Save.objects.filter(user=pk, video=obj)
            obj.is_saved = saves.count()
        queryset = sorted(queryset, key=lambda x: x.distance)
        recommended_videos_serializer = self.get_serializer(queryset, many=True)

        # adding is_liked and is_saved fields for video as it is in recomendation
        likes = Like.objects.filter(user=pk, video=instance)
        instance.is_liked = likes.count()
        saves = Save.objects.filter(user=pk, video=instance)
        instance.is_saved = saves.count()

        return Response({"video": serializer.data, "recomendation": recommended_videos_serializer.data})

class VideoCommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        comments = Comment.objects.filter(video=instance.id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)