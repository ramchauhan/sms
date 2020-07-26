from rest_framework import serializers

from accounts.serializers import UserListSerializer, UserCreateUpdateSerializer
from students.models import Student


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user']

    def get_user(self, obj):
        return UserListSerializer(instance=obj.user).data


class StudentUpdateSerializer(serializers.ModelSerializer):
    user = UserCreateUpdateSerializer()

    class Meta:
        model = Student
        read_only_fields = ['id', ]
        fields = [
            'id', 'user'
        ]

    def update(self, instance, validated_data):
        user = instance.user
        user.username = validated_data['user'].get('username', user.username)
        user.is_active = validated_data['user'].get('is_active', user.is_active)
        user.first_name = validated_data['user'].get('first_name', user.first_name)
        user.last_name = validated_data['user'].get('last_name', user.last_name)
        user.save()
        return instance
