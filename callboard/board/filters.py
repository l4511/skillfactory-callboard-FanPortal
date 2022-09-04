from django_filters import FilterSet, ChoiceFilter
from .models import Notice, Answer
from django import forms


class NoticeFilter(FilterSet):
    class Meta:
        model = Notice
        fields = ('notice_category',)


class AccountFilter(FilterSet):
    class Meta:
        model = Answer
        fields = ('answer_confirm',)
