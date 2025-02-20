from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from user.models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    #overide djoser's serializer

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["first_name","last_name","email","username","phone","password"]


