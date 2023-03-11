from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/resourses/', null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)
    distance = models.DecimalField(max_digits=12, decimal_places=6, null=True, default=0)
    is_liked = models.DecimalField(max_digits=1, decimal_places=0, null=True, default=0)
    is_saved = models.DecimalField(max_digits=1, decimal_places=0, null=True, default=0)

    def __str__(self):
        return self.title

    @property
    def user_detail(self):
        user = User.objects.get(id=self.user.id)
        return {"name": user.username,
                "email": user.email}

    @property
    def likes_amount(self):
        return self.likes.count()

    @property
    def saves_amount(self):
        return self.saves.count()

    @property
    def comments_amount(self):
        return self.comments.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    class Meta:
        unique_together = (("user", "video"),)

    def __str__(self):
        return self.user.username

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saves')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='saves')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True)

    def __str__(self):
        return self.comment

    @property
    def user_detail(self):
        user = User.objects.get(id=self.user.id)
        return {"name": user.username,
                "email": user.email}
