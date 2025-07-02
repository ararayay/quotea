from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Quotes(models.Model):
    quote = models.CharField(max_length=500)
    source = models.CharField(max_length=100)
    character = models.CharField(max_length=100)
    weight = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

class QuoteLike(models.Model):
    quote = models.ForeignKey(Quotes, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    vote_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])

    class Meta:
        unique_together = ('quote', 'ip_address')