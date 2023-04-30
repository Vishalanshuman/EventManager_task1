from .models import Event
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password']
        write_only_field = 'password1', 'password2',
        read_only_field = 'id'

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            first_name= validated_data['first_name'],
            last_name = validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'password']
  
    

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = 'owner',

