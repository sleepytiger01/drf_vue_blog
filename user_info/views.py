# user_info/views.py

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from user_info.serializers import UserRegisterSerializer, UserDetailSerializer
from user_info.permissions import IsSelfOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    # 详情地址不是主键值而是用户名了，这就是 lookup_field 发挥的作用
    # 与序列化器中的 lookup_field 要对应起来
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]

        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def info(self, request, username=None):
        queryset = User.objects.get(username=username)
        serializer = UserDetailSerializer(queryset, many=False)
        return Response(serializer.data)

    @action(detail=False)
    def sorted(self, request):
        users = User.objects.all().order_by('-username')

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
