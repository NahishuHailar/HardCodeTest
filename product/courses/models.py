from enum import unique
from django.db import models
from users.models import CustomUser


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Стоимость курса'
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступен для покупки'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка на видео',
    )
    course = models.ForeignKey(
        'Course',  
        on_delete=models.CASCADE,  
        related_name='lessons',  
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)  

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
        unique=True
    )
    course = models.ForeignKey(
        'Course',  
        on_delete=models.CASCADE,  
        related_name='groups',  
        verbose_name='Курс'
    )
    active = models.BooleanField(default=True)

    students = models.ManyToManyField(
        CustomUser,
        through='GroupMembership',
        related_name="student_groups",
        verbose_name='Студенты'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self):
        return self.title
    

class GroupMembership(models.Model):
    """Промежуточная модель для связи пользователя и группы."""
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Членство в группе'
        verbose_name_plural = 'Членства в группе'
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.get_full_name()} в группе {self.group.title}"