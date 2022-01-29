from .serializers import UserDataSerializer,UserProfileSerializer
from .models import UserProfile
import sys
import os



def auth_profile(token, user):
    type_user = None
    userprofile = None
    data = {}
    data['key'] = token.key
    data['user'] = UserDataSerializer(user).data
    data['student'] = False
    data['info'] = None
    info = {}
    def get_profile(profile):
        try:
            data_object = profile.objects.get(user=user)
            return data_object
        except:
            return None

    profile = get_profile(UserProfile)
    info['profile'] = UserProfileSerializer(profile).data 
    data['info'] = info
    return data