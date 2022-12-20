from django.db import models
from django.contrib.auth.models import User


class formInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Field = models.CharField(max_length=100, null=True)
    Amount = models.IntegerField(null=True)
