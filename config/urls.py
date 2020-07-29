from django.contrib import admin
from django.urls import path, include

from graphene_django.views import GraphQLView

from config.api import api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urls)),
    path("graphql", GraphQLView.as_view(graphiql=True)),
]
