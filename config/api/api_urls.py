from django.urls import include, path
from rest_framework import routers

from accounts import views as accounts_views
from students import views as student_views
from teachers import views as teacher_views

router = routers.DefaultRouter()
router.register(r'students', student_views.StudentViewSet, basename='students')
router.register(r'teachers', teacher_views.TeacherViewSet, basename='teachers')
router.register(
    r'auth', accounts_views.UserAuthenticationViewSet, basename='auth'
)

urlpatterns = [
    path('', include(router.urls)),
]
