from abc import ABC, ABCMeta

from rest_framework import serializers
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    firstname = serializers.CharField(write_only=True)
    lastname = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone = serializers.IntegerField(write_only=True)


class ResetPasswordEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
