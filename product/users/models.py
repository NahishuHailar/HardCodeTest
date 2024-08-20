from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name="Адрес электронной почты", max_length=250, unique=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name", "password")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-id",)

    def __str__(self):
        return self.email


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="balance",
        verbose_name="Пользователь",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=1000.00, verbose_name="Баланс"
    )

    class Meta:
        verbose_name = "Баланс"
        verbose_name_plural = "Балансы"
        ordering = ("-id",)

    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValueError("Баланс не может быть ниже 0.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()}: {self.amount} бонусов"


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="subscriptions"
    )
    date_subscribed = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("-id",)
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.title}"
