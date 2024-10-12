from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'last_modified', 'user']
        read_only_fields = ['id', 'created_at', 'last_modified', 'user']  # 'user' will be automatically set to the logged-in user

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user  # Set the user from the request
        return super().create(validated_data)
