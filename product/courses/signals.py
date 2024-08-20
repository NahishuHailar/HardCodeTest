from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Subscription


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    Происходит в UsersCourseViewset в методе assign_to_group
    для более наглядного поведения бизнес логики:  
    "Списание средств с баланса" --> "Создание подписки" --> "Распределение пользователя в группу"
    Работу с сигналами можно посмотреть users.signals

    """

    if created:
        pass
        # TODO