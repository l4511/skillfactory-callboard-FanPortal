import datetime
from django.db.models.signals import post_save, pre_save, m2m_changed, post_init
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Notice, Answer
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.models import User


@receiver(post_save, sender=Answer)
def send_mail_answer(sender, instance, created, **kwargs):
    if created:
        user = Notice.objects.get(pk=instance.answer_post_id).notice_user
        send_mail(
            subject='Новый отклик',
            message=f'{instance.answer_user} оставил отклик на Ваше объявление: {instance.answer_text}',
            from_email='alexgoldm1991@yandex.ru',
            recipient_list=[User.objects.filter(username=user).values("email")[0]['email']],
        )
