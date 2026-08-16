from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True)
    category = models.ForeignKey(
        Category, related_name="articles", on_delete=models.SET_NULL, null=True, blank=True
    )
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.slug])