from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # task_set


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
