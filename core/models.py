from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Movie(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    genres = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Collection(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return str(self.uuid)
