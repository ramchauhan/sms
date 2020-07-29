import graphene

from graphene_django import DjangoObjectType

from students.graphql.query import StudentType
from teachers.models import Teacher


class TeacherType(DjangoObjectType):
    students = graphene.List(StudentType)
    class Meta:
        model = Teacher
        fields = ("id", "user")

    def resolve_students(self, info):
        return [rating.student for rating in self.raitings.all()]


class TeachersQuery(graphene.ObjectType):
    teachers = graphene.List(TeacherType)

    def resolve_teachers(self, info):
        return Teacher.objects.all()
