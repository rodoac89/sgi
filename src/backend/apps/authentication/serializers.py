# from rest_framework import serializers
# from .models import UserProfile
# from django.contrib.auth.models import User


# class UserDataSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     date_joined = serializers.DateTimeField()
#     last_login = serializers.DateTimeField() 

#     class Meta:
#         model = User

# class UserProfileSerializer(serializers.Serializer):
#     user = serializers.StringRelatedField()
#     image_profile = serializers.ImageField()
#     since = serializers.DateTimeField()
#     role = serializers.StringRelatedField(many=True)
#     class Meta:
#         model = UserProfile

