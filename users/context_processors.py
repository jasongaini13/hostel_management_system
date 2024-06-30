# users/context_processors.py

from .models import CloakRoomSettings

def cloak_room_settings(request):
    settings = CloakRoomSettings.objects.first()
    return {
        'settings': settings
    }
