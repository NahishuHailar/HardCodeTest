from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription, Balance
from courses.models import Group, GroupMembership

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = fields = (
            'first_name',
            'last_name',
            'email',
        )        

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

class GroupWithStudentsSerializer(serializers.ModelSerializer):
    """Группы с вложенными данными студентов."""

    students = serializers.SerializerMethodField()
    course = serializers.StringRelatedField()

    class Meta:
        model = Group
        fields = ('title', 'course', 'students')

    def get_students(self, obj):
        """Получить список студентов в группе."""
        memberships = GroupMembership.objects.filter(group=obj).select_related('user')
        return StudentSerializer([membership.user for membership in memberships], many=True).data