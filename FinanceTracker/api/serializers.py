
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Goal
        fields = ["id", "user", 'income', 'saving', 'date_created']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "user", "name"]
        extra_kwargs = {"user": {"read_only": True}}


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    class Meta:
        model = Expense
        fields = ["id", "user", "category", "category_id","name",
                  "description", "amount", "date_created"]
        extra_kwargs = {"user": {"read_only": True}}
