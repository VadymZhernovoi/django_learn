from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django_learn.settings import DEFAULT_FROM_EMAIL
from .models import Task
from .enums import Status


def _owner_email(task: Task):
    owner = getattr(task, "owner", None)
    email = getattr(owner, "email", None)
    return email or None


@receiver(pre_save, sender=Task)
def task_pre_save_capture_old_status(sender, instance: Task, **kwargs):
    """
    Перед сохранением задачи читаем её предыдущий статус из БД и кладём в _old_status
    """
    if instance.pk:
        try:
            old = Task.objects.get(pk=instance.pk)
            instance._old_status = old.status
        except Task.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Task)
def task_post_save_notify(sender, instance: Task, created: bool, **kwargs):
    """
    Отправляем уведомления только при смене статуса.
    Защита от повторов: не шлём, если статус не поменялся.
    """
    # email владельца
    to_email = _owner_email(instance)
    if not to_email:
        return

    old_status = getattr(instance, "_old_status", None)
    new_status = instance.status

    # Статус не менялся — не уведомляем.
    if old_status == new_status:
        return

    if created:
        subject = "Task created"
        message = f"Task '{instance.title}' has been created."
    elif new_status == Status.DONE:
        subject = "Task closed"
        message = f"Task '{instance.title}' has been closed."
    else:
        subject = "Task status changed"
        message = f"Task '{instance.title}' status changed: {old_status} -> {new_status}."

    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", DEFAULT_FROM_EMAIL),
        [to_email],
        fail_silently=True,
    )