from decimal import Decimal
from django.core.exceptions import ValidationError

def validate_amount(amount):
    if not amount:
        raise ValidationError("Сумма бонусов обязательна для указания.")
    try:
        amount = Decimal(amount)
    except ValueError:
            raise ValidationError("Сумма бонусов должна быть числом.")

    if amount <= 0:
        raise ValidationError("Сумма бонусов должна быть положительной.")