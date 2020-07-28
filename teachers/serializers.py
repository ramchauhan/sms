from django.contrib.auth import get_user_model

from rest_framework import serializers

from accounts.serializers import UserListSerializer, UserCreateUpdateSerializer
from students.models import Student
from teachers.models import Teacher

User = get_user_model()


class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'students']

    def get_user(self, obj):
        return UserListSerializer(instance=obj.user).data


class TeacherAttachStudentSerializer(serializers.ModelSerializer):
    students_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=Student.objects.all(), source='students'
    )

    class Meta:
        model = Teacher
        fields = ['students_ids']


class TeacherUpdateSerializer(serializers.ModelSerializer):
    user = UserCreateUpdateSerializer()

    class Meta:
        model = Teacher
        read_only_fields = ['id', ]
        fields = [
            'id', 'user',
        ]

    def update(self, instance, validated_data):
        user = instance.user
        user.username = validated_data['user'].get('username', user.username)
        user.is_active = validated_data['user'].get('is_active', user.is_active)
        user.first_name = validated_data['user'].get('first_name', user.first_name)
        user.last_name = validated_data['user'].get('last_name', user.last_name)
        user.save()
        return instance


class RateStudentSerializer(serializers.Serializer):
    student_id = serializers.ListSerializer(
        child=serializers.IntegerField(),
        allow_empty=False
    )

    def validate(self, attrs):
        students = self.context['instance'].students.filter(
            id__in=attrs['student_id']
        )
        if students.count() != len(attrs['student_id']):
            student_ids_diff = (
                set(attrs['student_id']) - set(
                    students.values_list('id', flat=True)
                )
            )
            raise serializers.ValidationError(
                f"{student_ids_diff} are not valid Student IDs"
            )

        attrs['students'] = students
        return attrs
