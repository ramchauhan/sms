import graphene

from accounts.graphql.query import UserQuery
from students.graphql.query import StudentQuery
from teachers.graphql.query import TeachersQuery

class Query(UserQuery, TeachersQuery, StudentQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
