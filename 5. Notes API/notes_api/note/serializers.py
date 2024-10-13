from .models import Note, Tag
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(source='owner.email',read_only=True)
    class Meta:
        model = Tag
        fields = ['id', 'name', 'owner']
        read_only_fields= ['id', 'owner']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)

class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(source='owner.email',read_only=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),  # Accept a list of strings for tags
        write_only=True
    )
    tag_names = serializers.SerializerMethodField()
    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'tags', 'tag_names', 'owner', 'created_at', 'last_modified']
        read_only_fields= ['id', 'owner', 'created_at', 'last_modified']

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        tags_data = validated_data.pop('tags',[])
        note = Note.objects.create(**validated_data)
        self._update_tags(note,tags_data)
        return note
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags',[])
        instance = super().update(instance, validated_data)
        self._update_tags(instance,tags_data)
        current_tags = list(instance.tags.all())
        for tag in current_tags:
            if not tag.notes.filter(owner=instance.owner).exists():
                tag.delete()
        return instance
    
    def _update_tags(self, note, tags_data):
        user = note.owner
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name.capitalize(), owner=user)
            tags.append(tag)
        note.tags.set(tags)

    def delete(self, instance):
        tags = instance.tags.all()
        super().delete(instance)
        for tag in tags:
            if not tag.notes.filter(owner=instance.owner).exists():
                tag.delete()