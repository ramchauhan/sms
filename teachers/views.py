from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from students.models import Student
from teachers.models import Teacher, Rating
from teachers.serializers import (
    TeacherSerializer, TeacherAttachStudentSerializer,
    TeacherUpdateSerializer, RateStudentSerializer
)


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Teacher.objects.all().order_by(
        'user__first_name'
    ).select_related('user')
    serializer_class = TeacherSerializer
    ordering = ['first_name']

    def get_queryset(self):
        if self.request.user.user_type == 'T':
            return self.queryset.filter(user=self.request.user)

        return self.queryset

    def get_serializer_class(self):
        if self.action == "attach_students":
            return TeacherAttachStudentSerializer

        if self.action == "rate_students":
            return RateStudentSerializer

        if self.request.method in ('POST', 'PUT'):
            return TeacherUpdateSerializer

        return self.serializer_class

    @action(methods=['POST', ], detail=True,
        permission_classes=[IsAuthenticated,])
    def attach_students(self, request, pk=None):
        teacher = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        staudents = Student.objects.filter(id__in=request.data['students_ids'])
        teacher.students.add(*staudents)
        data = {'success': 'Sucessfully Added'}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST', ], detail=True,
        permission_classes=[IsAuthenticated,])
    def rate_students(self, request, pk=None):
        teacher = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(
            data=request.data, context={"instance": teacher, "request": request}
        )
        serializer.is_valid(raise_exception=True)

        for student in serializer.validated_data['students']:
            Rating.objects.get_or_create(
                teacher=teacher, student=student
            )

        data = {'success': 'Marked Star Student successfully'}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
