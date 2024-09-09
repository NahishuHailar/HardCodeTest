from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from yaml import serialize

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.user_serializer import GroupWithStudentsSerializer
from api.v1.serializers.course_serializer import (
    BasicCourseSerializer,
    CreateCourseSerializer,
    CreateGroupSerializer,
    CreateLessonSerializer,
    DetailedCourseSerializer,
    GroupSerializer,
    LessonSerializer,
    PurchaseCourseSerializer,
    UserCourseSerializer,
)

from api.v1.services.course_view_serv import students_to_group, make_payment
from courses.models import Course, Group, GroupMembership, Lesson
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LessonSerializer 
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_id")
        serializer.save(course_id=course_id)

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs.get("course_id"))


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return GroupSerializer
        return CreateGroupSerializer

   
    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_id")
        serializer.save(course_id=course_id)


    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return Group.objects.filter(course_id=course_id)


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы. Администрирование курсов."""

    queryset = Course.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        """
        Параметр include_stats=true для статистики по курсам(доп задание).
        """
        if self.action in ["list", "retrieve"]:
            if self.request.query_params.get("include_stats") == "true":
                return DetailedCourseSerializer  # Доп информация по курсам
            return BasicCourseSerializer  # Базовая информация по курсам
        return CreateCourseSerializer

    @action(detail=True, methods=["get"])
    def groups(self, request, pk=None):
        """Получить список пользователей в группах курса(доп задание)."""

        course = get_object_or_404(Course, id=self.kwargs.get("pk"))
        groups = Group.objects.filter(course=course).prefetch_related(
            "memberships__user"
        )
        serializer = GroupWithStudentsSerializer(groups, many=True)
        return Response(serializer.data)


class UsersCourseViewset(viewsets.ModelViewSet):
    """Курсы для юзера. Список доступных курсов.
    Покупка курса.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "head", "options"]

    def get_serializer_class(self):
        return UserCourseSerializer

    def get_queryset(self):
        """Курсы доступные пользователю."""
        user = self.request.user
        purchased_courses = Subscription.objects.filter(user=user).values_list(
            "course_id", flat=True
        )
        return Course.objects.filter(is_available=True).exclude(
            id__in=purchased_courses
        )

    @action(detail=True, methods=["get"])
    def pay(self, request, pk=None):
        """Покупка доступа к курсу (подписка на курс)."""
        return make_payment(self, request, pk)
