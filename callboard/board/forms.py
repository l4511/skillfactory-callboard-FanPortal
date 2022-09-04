from django.forms import ModelForm
from .models import Notice, Answer
from django import forms


class NoticeForm(ModelForm):
    notice_header = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
    notice_text = forms.CharField(label='Текст', widget=forms.TextInput(attrs={'class': 'form-input'}))
    notice_video = forms.CharField(label='Ссылка на видео YouTube',
                                   widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
    notice_image = forms.ImageField(label='Изображение или картинка', required=False)

    class Meta:
        model = Notice
        fields = ['notice_user', 'notice_header', 'notice_text', 'notice_video', 'notice_category', 'notice_image']
        widgets = {
            'notice_user': forms.HiddenInput(),
        }


class AnswerForm(ModelForm):
    answer_text = forms.CharField(label='Текст', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Answer
        fields = ('answer_text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
