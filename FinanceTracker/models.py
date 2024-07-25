from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class Category (models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Category by {self.user.username}  {self.name}"


class Expense (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense by {self.user.username} category {self.category}"


class Goal (models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="goals")
    income = models.FloatField()
    saving = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Goal by {self.user.username}"
