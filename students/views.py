from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from students.models import Student
from students.serializers import StudentSerializer, StudentUpdateSerializer


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all().order_by('user__first_name').select_related('user')
    serializer_class = StudentSerializer
    ordering = ['first_name']

    def get_queryset(self):
        if self.request.user.user_type == 'S':
            return self.queryset.filter(user=self.request.user)

        return self.queryset

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return StudentUpdateSerializer

        return self.serializer_class
