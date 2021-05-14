
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CreateUser,Advisor


class Registration(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields=['advisor_name','advisor_image']        

class UserSerializer(serializers.ModelSerializer):
    advise = AdvisorSerializer(many=True)

    class Meta:
        model = CreateUser
        fields = ['user','advise']        