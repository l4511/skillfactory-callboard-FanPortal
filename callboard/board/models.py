from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.category}'


class Notice(models.Model):
    notice_header = models.CharField(max_length=255)
    notice_text = models.TextField()
    notice_video = models.TextField(null=True, blank=True)
    notice_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория объявления')
    notice_time_create = models.DateTimeField(auto_now_add=True)
    notice_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice_user')
    notice_image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.notice_header}'

    def get_absolute_url(self):
        return f'/notice/{self.id}'


class Answer(models.Model):
    answer_post = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='answer')
    answer_user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255,  verbose_name='Текст ответа')
    answer_time_create = models.DateTimeField(auto_now_add=True)
    answer_confirm = models.BooleanField(default=False, verbose_name='Комментарий принят')

    class Meta:
        unique_together = ('answer_post', 'answer_user')

    def __str__(self):
        return f'{self.answer_text}'

    def is_accept(self):
        return self.answer_confirm
