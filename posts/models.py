from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)


class Subject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ["title", "category"]
        ]