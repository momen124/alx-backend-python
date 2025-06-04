from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access if user is a participant in the conversation
        return obj.participants.filter(id=request.user.id).exists()