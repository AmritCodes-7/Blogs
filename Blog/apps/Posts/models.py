from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Blogs(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to="blog_images/", blank=True, null=True)

    def __str__(self):
        return self.title
