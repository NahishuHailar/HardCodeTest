from django.core.exceptions import ValidationError
from django.db.models import Count

from courses.models import GroupMembership, Group


def students_to_group(self, user, course):
    """Распределение студента в группу равномерно с учетом ограничений."""
    # Определяем максимальное количество групп и студентов в группе
    max_groups = 10
    max_students_per_group = 30

    # Получаем все группы для данного курса и аннотируем количество студентов
    groups = course.groups.annotate(num_students=Count('memberships')).order_by('num_students')

    # Проверяем, есть ли свободные группы
    available_group = groups.filter(num_students__lt=max_students_per_group).first()

    if available_group:
        # Если найдена подходящая группа, добавляем пользователя
        GroupMembership.objects.create(user=user, group=available_group)
    else:
        # Если нет доступных групп, проверяем количество групп
        if groups.count() < max_groups:
            # Создаем новую группу
            new_group = Group.objects.create(course=course, title=f"Group {groups.count() + 1}")
            GroupMembership.objects.create(user=user, group=new_group)
        else:
            raise ValidationError("Все группы заполнены. Невозможно создать новую группу.")
    