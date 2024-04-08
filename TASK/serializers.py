from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        exclude=['created_at','updated_at']
        
    