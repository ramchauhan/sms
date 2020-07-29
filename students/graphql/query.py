import graphene

from graphene_django import DjangoObjectType

from students.models import Student


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = ("id", "user")


class StudentQuery(graphene.ObjectType):
    students = graphene.List(StudentType)

    def resolve_students(self, info):
        return Student.objects.all()
