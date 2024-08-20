from django.contrib import admin
from courses.models import Course, Lesson, Group, GroupMembership


@admin.register(Course)
class BalanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "title",
        "start_date",
        "price",
        "is_available",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "link",
        "course",
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "course",
        "active",
    )


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "group",
        "date_joined",
    )
