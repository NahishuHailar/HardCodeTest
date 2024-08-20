# Generated by Django 4.2.10 on 2024-08-20 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmembership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_memberships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='courses.course', verbose_name='Курс'),
        ),
        migrations.AddField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(related_name='student_groups', through='courses.GroupMembership', to=settings.AUTH_USER_MODEL, verbose_name='Студенты'),
        ),
        migrations.AlterUniqueTogether(
            name='groupmembership',
            unique_together={('user', 'group')},
        ),
    ]
