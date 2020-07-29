import graphene

from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class UserQuery(graphene.ObjectType):
    user = graphene.List(UserType)

    def resolve_user(self, info):
        return User.objects.all()
