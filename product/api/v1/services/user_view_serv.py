from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from users.models import Balance
 

User = get_user_model()

def validate_amount(amount):
    """Валидация бонусов"""
    if not amount:
        raise ValidationError("Сумма бонусов обязательна для указания.")
    try:
        amount = Decimal(amount)
    except ValueError:
            raise ValidationError("Сумма бонусов должна быть числом.")

    if amount <= 0:
        raise ValidationError("Сумма бонусов должна быть положительной.")
    

def get_bonus(request, pk):
    """Начисление бонусов"""
    amount = request.data.get('amount')
    validate_amount(amount)
       
    user = get_object_or_404(User, pk=pk)

    # Начисление бонусов
    balance, created = Balance.objects.get_or_create(user=user)
    balance.amount += amount
    balance.save()

    return Response({
            "message": f"Бонусы в размере {amount} успешно начислены пользователю {user.get_full_name()}",
            "new_balance": balance.amount
        })    
         