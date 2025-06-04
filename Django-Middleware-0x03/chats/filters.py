import django_filters
from .models import Message
from django.contrib.auth.models import User

class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.ModelChoiceFilter(queryset=Conversation.objects.all())
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    start_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'start_date', 'end_date']