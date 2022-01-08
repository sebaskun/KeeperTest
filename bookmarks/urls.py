from rest_framework import routers
from django.urls import path, include

from .views import BookmarkViewSet, CreateUserView

router = routers.DefaultRouter()
router.register(r'bookmark', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('api/', include((router.urls, 'api'), namespace='api_keeper')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/register', CreateUserView.as_view()),
]