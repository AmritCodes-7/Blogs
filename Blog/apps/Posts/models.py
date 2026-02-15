from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify


class PublishedStatus(models.TextChoices):
    PUBLISHED = "published", "Published"
    DRAFT = "draft", "Draft"


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
    publish_status = models.CharField(
        choices=PublishedStatus.choices, max_length=9, default=PublishedStatus.PUBLISHED
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        indexes = [
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


class ReadList(models.Model):
    """
    A collection of blog posts saved by a user for later reading
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="readlist")
    title = models.CharField(max_length=50)
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Describe what this reading list is about",
    )
    created_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=150)
    is_public = models.BooleanField(
        default=False,
        help_text="Make this list visible to other users",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Reading List"
        verbose_name_plural = "Reading Lists"
        unique_together = ["user", "title"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.user.username}-{self.title}")
            slug = base_slug
            counter = 1
            while ReadList.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} by {self.title}"


class ReadListItem(models.Model):
    readlist = models.ForeignKey(
        ReadList, on_delete=models.CASCADE, related_name="items"
    )
    blog = models.ForeignKey(
        Blogs, on_delete=models.CASCADE, related_name="saved_in_lists"
    )
    added_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "ReadListItem"
        verbose_name_plural = "ReadListItems"
        ordering = ["position", "-added_at"]
        unique_together = ["readlist", "blog"]
        indexes = [
            models.Index(fields=["readlist", "position"]),
            models.Index(fields=["readlist", "is_read"]),
        ]

    def __str__(self):
        return f"{self.blog.title} in {self.readlist.title}"
