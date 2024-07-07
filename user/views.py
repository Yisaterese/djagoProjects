from rest_framework.generics import CreateAPIView

from user.models import User
from user.serializers import UserCreateSerializer

#
# class UserRegister(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer