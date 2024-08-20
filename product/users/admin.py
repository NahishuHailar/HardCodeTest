from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, Balance, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "username", "first_name", "last_name", "password")


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "date_subscribed", "active")
