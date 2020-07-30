import graphene

from graphene_django import DjangoObjectType

from teachers.models import Teacher, Rating


class StarStudentMutation(graphene.Mutation):
    class Arguments:
        teacher_id = graphene.Int(required=True)
        student_ids = graphene.List(graphene.Int)
        mark_star = graphene.Boolean(required=True)

    message = graphene.String()
    error_messages = graphene.String()

    def mutate(self, info, student_ids, teacher_id, mark_star):
        if not student_ids:
            return StarStudentMutation(
                error_messages=f"At least one student should be provided"
            )

        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return StarStudentMutation(
                error_messages=f"Teacher with id = {teacher_id} DoesNotExist"
            )

        students = [st.id for st in teacher.students.all()]
        student_ids_diff = set(student_ids) - set(students)
        if student_ids_diff:
            return StarStudentMutation(
                error_messages=f"Student with ids = {student_ids_diff}," +
                " does not belongs to provided Teacher"
            )

        if mark_star:
            for id in students:
                Rating.objects.get_or_create(student_id=id, teacher=teacher)

            return StarStudentMutation(message="Students Starred Successfully")
        else:
            for id in students:
                Rating.objects.filter(teacher=teacher, student_id=id).delete()

        return StarStudentMutation(message="Students Unstarred Successfully")


class StudentMutation(graphene.ObjectType):
    star_student = StarStudentMutation.Field()
