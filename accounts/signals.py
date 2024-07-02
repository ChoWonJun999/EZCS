from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserSession


@receiver(post_save, sender=UserSession)
def mymodel_post_save_handler(sender, instance, created, **kwargs):
    if created:
        print(f"새로운 MyModel 인스턴스가 생성되었습니다: {instance}")
    else:
        print(f"MyModel 인스턴스가 업데이트되었습니다: {instance}")