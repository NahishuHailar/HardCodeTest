from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription, Balance

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор Подписки."""

    class Meta:
        model = Subscription
        fields = ('user', 'course', 'date_subscribed', 'active', 'expiration_date')


class BalanceSerializer(serializers.ModelSerializer):
    """Сериализатор Баланса."""

    class Meta:
        model = Balance
        fields = ('user', 'amount')

class StudentSerializer(serializers.ModelSerializer):
    """Сериализатор Студентов курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )        