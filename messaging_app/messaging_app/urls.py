from django.contrib import admin
from django.urls import path, include  # include added

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # include the chats app URLs here
]

