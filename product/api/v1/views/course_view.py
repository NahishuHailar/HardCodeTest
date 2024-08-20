from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
 
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin
from api.v1.serializers.course_serializer import (
    BasicCourseSerializer,
    CreateCourseSerializer,
    CreateGroupSerializer,
    CreateLessonSerializer,
    DetailedCourseSerializer,
    GroupSerializer,
    LessonSerializer, 
    PurchaseCourseSerializer,
    StudentSerializer,
    UserCourseSerializer,
    )

from courses.models import Course, Group, GroupMembership    
from users.models import Subscription
from api.v1.services.course_view_serv import students_to_group


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()



class CourseViewSet(viewsets.ModelViewSet):
    """Курсы. Администрирование курсов."""

    queryset = Course.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        """
        Параметр include_stats=true для статистики по курсам(доп задание).
        """
        if self.action in ['list', 'retrieve']:
            if self.request.query_params.get('include_stats') == 'true':
                return DetailedCourseSerializer # Доп информация по курсам
            return BasicCourseSerializer # Базовая информация по курсам
        return CreateCourseSerializer

    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        """Получить список пользователей в группах курса(доп задание)."""

        course = get_object_or_404(Course, id=self.kwargs.get('pk')) 
        groups = Group.objects.filter(course=course).prefetch_related('memberships__user')
        memberships = GroupMembership.objects.filter(group__in=groups).select_related('user')
        users = [membership.user for membership in memberships]

        serializer = StudentSerializer(users, many=True)
        return Response(serializer.data)


class UsersCourseViewset(viewsets.ModelViewSet):
    """Курсы. Для юзера. Список доступных курсов, Покупка"""
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']
    serializer_class = UserCourseSerializer  

    def get_serializer_class(self):
        if self.action in ['post',]:
            return PurchaseCourseSerializer 
        return UserCourseSerializer 


    def get_queryset(self):
        """Курсы доступные пользователю."""
        user = self.request.user
        purchased_courses = Subscription.objects.filter(user=user).values_list('course_id', flat=True)
        return Course.objects.filter(
            is_available=True
        ).exclude(
            id__in=purchased_courses
        )
    
    def list(self, request):
        """Список доступных для покупки курсов."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """Покупка доступа к курсу (подписка на курс)."""

        course = self.get_object()
        user = request.user
        balance = user.balance

        if balance.amount < course.price:
            raise ValidationError("Недостаточно средств на балансе")

        try:
            with transaction.atomic():
                # Списание средств с баланса
                balance.amount -= course.price
                balance.save()

                # Создание подписки (Получение доступа к курсу)
                subscription, created = Subscription.objects.get_or_create(user=user, course=course)

                # Распределение пользователя в группу
                self.assign_to_group(user, course)

            return Response(
                data={"message": "Подписка на курс успешно оформлена"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            raise ValidationError(f"Ошибка при оформлении подписки: {str(e)}")
    

    def assign_to_group(self, user, course):
        """Распределение студента в группу равномерно с учетом ограничений."""
        students_to_group(self, user, course)
    
