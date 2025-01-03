from django.db import models
from django.utils.timezone import now


# Create your models here.
class UserIncome(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ["-date"]


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
