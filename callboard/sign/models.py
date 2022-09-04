from django.contrib.auth.models import User
from django.db import models


class UserCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='valid_user')
    code = models.IntegerField()
    valid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.valid}'
