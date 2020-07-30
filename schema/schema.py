import graphene

from accounts.graphql.query import UserQuery
from students.graphql.query import StudentQuery
from teachers.graphql.query import TeachersQuery
from teachers.graphql.mutations import StudentMutation


class Query(UserQuery, TeachersQuery, StudentQuery, graphene.ObjectType):
    pass


class Mutation(StudentMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
