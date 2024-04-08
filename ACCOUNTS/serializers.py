from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import APIException, AuthenticationFailed
from unittest import mock
from datetime import timedelta
class RegisterSerialzer(serializers.Serializer):
    
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    password=serializers.CharField()
    username=serializers.CharField()
    
    extra_kwargs = {
            'password':{'write_only':True}
        }
    def validate(self, data):
        
        if User.objects.filter(username=data['username']).exists():
           raise serializers.ValidationError('username is taken')
       
        return data
    
    def create(self, validated_data):
        user=User.objects.create(first_name=validated_data['first_name'],
                                last_name=validated_data['last_name'],
                                username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()
        # instance=self.User(**validated_data)
        # instance.save()
        # print(user.password)
        return validated_data
        
        
        
class LoginSerialzer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        
        return data
    
    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            return {'message': "Invalid credentials", 'data': {}}
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        
        access_token_lifetime = timedelta(hours=24) 
        
        # Set token expiration
        refresh.set_exp(lifetime=access_token_lifetime)
        access_token_payload = {
            'token': {
                'refresh': str(refresh),
                'access': access_token
            }
        }
        return {'message': "Login successful", 'data': access_token_payload}
        
        