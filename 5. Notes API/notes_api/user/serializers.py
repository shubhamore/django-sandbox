from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'is_active', 'is_staff', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            # 'first_name': {'required': True},
            # 'last_name': {'required': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            'date_joined': {'read_only': True},
        }

    def create(self, validated_data):
        # Create a new user with a hashed password
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])  # Hash the password before saving
        user.save()
        return user

    def update(self, instance, validated_data):
        # Update user and handle password hashing
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)  # Hash the password if provided

        instance.save()
        return instance
