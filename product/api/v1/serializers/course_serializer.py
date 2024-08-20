from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import serializers

from courses.models import Course, Group, Lesson

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    class Meta:
        model = Group
        fields = '__all__'


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )

class BasicCourseSerializer(serializers.ModelSerializer):
    """Базовая информация о курсе."""
    
    lessons_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
        )

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()


class DetailedCourseSerializer(serializers.ModelSerializer):
    """Информация о курсе со статистикой."""
    
    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()
    
    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        return obj.subscriptions.count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел."""
        max_students_per_group = 30
        groups = obj.groups.annotate(num_students=Count('students'))

        if not groups:
            return 0

        total_fill_percentage = sum(
        (group.num_students / max_students_per_group) * 100 for group in groups
        )

        return total_fill_percentage / len(groups)

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        total_users = User.objects.count()
        if total_users == 0:
            return 0

        purchase_count = obj.subscriptions.count()
        return (purchase_count / total_users) * 100



class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = '__all__'


class UserCourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'start_date', 'price', 'is_available', 'lesson_count']

    def get_lesson_count(self, obj):
        return obj.lessons.count()
    

class PurchaseCourseSerializer(serializers.ModelSerializer):
      class Meta:
        model = Course
        fields = ['title']
        