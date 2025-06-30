from django.db import models


class Quotes(models.Model):
    quote = models.CharField(max_length=500)
    source = models.CharField(max_length=100)
    character = models.CharField(max_length=100)
    weight = models.IntegerField()
    views = models.IntegerField()
    likes = models.IntegerField()
    dislikes = models.IntegerField()
