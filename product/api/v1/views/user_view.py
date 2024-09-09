from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Balance
from api.v1.serializers.user_serializer import CustomUserSerializer, BalanceSerializer
from api.v1.services.user_view_serv import get_bonus

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserBonusViewSet(viewsets.ViewSet):
    """Вьюсет для работы с балансом текущего пользователя."""

    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        """Просмотр баланса текущего пользователя."""
        user = request.user

        balance = Balance.objects.get(user=user)
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)


class AdminBonusViewSet(viewsets.ViewSet):
    """Вьюсет для работы с балансами пользователей.
    Доступен только администраторам."""

    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["get", "post", "head", "options"]

    def list(self, request):
        """Просмотр всех балансов."""
        balances = Balance.objects.all()
        serializer = BalanceSerializer(balances, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Просмотр баланса конкретного пользователя."""
        balance = get_object_or_404(Balance, user_id=pk)
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_bonus(self, request, pk=None):
        """Начисление бонусов пользователю."""
        return get_bonus(request, pk)
      