from .models import Note
from rest_framework import serializers

class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(source='owner.email',read_only=True)
    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'owner', 'created_at', 'last_modified']
        read_only_fields= ['id', 'owner', 'created_at', 'last_modified']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)