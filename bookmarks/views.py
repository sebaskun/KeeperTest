from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .permissions import BookmarkPermissions
from .serializers import (
    BookmarkSerializer,
    BookmarkSerializerUpdate,
    UserSerializer
)
from .models import *

User = get_user_model()


# Create your views here.
class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, BookmarkPermissions]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.queryset.filter(private=False)
        return self.queryset.filter(Q(owner=self.request.user)|Q(private=False))

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ['PUT', 'PATCH']:
            serializer_class = BookmarkSerializerUpdate

        return serializer_class

class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer