from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify


class Blogs(models.Model):
    title = models.CharField(max_length=200)
    body = CKEditor5Field("Content", config_name="default")
    featured_image = models.ImageField(
        upload_to="blog_images/",
        blank=True,
        null=True,
        help_text="Upload a featured image for your blog post",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, max_length=250)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Handle duplicate slugs
            while Blogs.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
