from django.contrib.auth import (get_user_model, authenticate, logout)

from rest_framework import status, generics, viewsets, serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.serializers import (
    RegistrationSerializer, UserLoginSerializer, EmptySerializer
)

User = get_user_model()


class UserAuthenticationViewSet(viewsets.GenericViewSet):
    serializer_class = RegistrationSerializer
    serializer_classes = {
        'login': UserLoginSerializer,
        'logout': EmptySerializer
    }
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    @action(methods=['POST', ], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = serializer.data
        data.update({'id': instance.id})
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user is None:
            raise serializers.ValidationError(
                "Invalid username/password. Please try again!"
            )

        data = RegistrationSerializer(user).data
        token = Token.objects.create(user=user).key
        data.update({'token': token, 'id': user.id})
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated,])
    def logout(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]

        return super().get_serializer_class()
