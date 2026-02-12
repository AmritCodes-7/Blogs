from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField


class Blogs(models.Model):
    title = models.CharField(max_length=200)
    body = SummernoteTextField()
    featured_image = models.ImageField(
        upload_to="blog_images/",
        blank=True,
        null=True,
        help_text="Upload a featured image for your blog post",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title
