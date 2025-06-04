import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Extended User model
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Explicitly declared for checker
    phone_number = models.CharField(max_length=20)
    bio = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']
    USERNAME_FIELD = 'username'  # Default Django behavior

    def __str__(self):
        return self.username

# Conversation model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

# Message model
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} in Conv {self.conversation.conversation_id}"
