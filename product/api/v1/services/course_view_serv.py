from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count

from rest_framework.response import Response
from rest_framework import status
from courses.models import GroupMembership, Group
from users.models import Subscription


def students_to_group(user, course):
    """Распределение студента в группу равномерно с учетом ограничений."""
    # Определяем максимальное количество групп и студентов в группе
    max_groups = 10
    max_students_per_group = 30

    # Получаем все группы для данного курса и аннотируем количество студентов
    groups = course.groups.annotate(num_students=Count("memberships")).order_by(
        "num_students"
    )

    # Проверяем, есть ли свободные группы
    available_group = groups.filter(num_students__lt=max_students_per_group).first()

    if available_group:
        # Если найдена подходящая группа, добавляем пользователя
        GroupMembership.objects.create(user=user, group=available_group)
    else:
        # Если нет доступных групп, проверяем количество групп
        if groups.count() < max_groups:
            # Создаем новую группу
            new_group = Group.objects.create(
                course=course, title=f"{course.title} Group {groups.count() + 1}"
            )
            GroupMembership.objects.create(user=user, group=new_group)
        else:
            raise ValidationError(
                "Все группы курса заполнены. Невозможно создать новую группу."
            )


def make_payment(instance, request, pk):
    """Оплата курса"""
    course = instance.get_object()
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
            subscription, created = Subscription.objects.get_or_create(
                user=user, course=course
            )
            if not created:
                # Подписка уже существует, откатываем транзакцию и поднимаем ошибку
                raise ValidationError("Вы уже подписаны на этот курс")

            # Распределение пользователя в группу
            students_to_group(user, course)

            return Response(
                data={"message": "Подписка на курс успешно оформлена"},
                status=status.HTTP_201_CREATED,
            )
    except Exception as e:
        return Response(
            data={"error": f"Ошибка при оформлении подписки: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
