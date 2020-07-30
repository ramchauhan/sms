from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'user_type', 'first_name', 'last_name',
            'password', 'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("passwords are not matching")

        return attrs

    def save(self):
        instance = User(
            email=self.validated_data['email'],
            user_type=self.validated_data['user_type'],
            username=self.validated_data.get('username'),
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data.get('last_name')
        )
        password = self.validated_data['password']

        instance.set_password(password)
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'user_type', 'first_name', 'last_name',
            'is_active'
        ]

    def get_user_type(self, obj):
        return obj.get_user_type_display()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60, required=True)
    password = serializers.CharField(required=True, write_only=True)


class EmptySerializer(serializers.Serializer):
    pass


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['id', 'user_type', 'email']
        fields = [
            'id', 'email', 'username', 'user_type', 'first_name', 'last_name',
            'is_active'
        ]
