from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .Views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'conversations/(?P<conversation_conversation_id>[^/.]+)/messages', MessageViewSet, basename='message')
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]