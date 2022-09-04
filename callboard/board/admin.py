from django.contrib import admin
from .models import Notice, Category, Answer
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NoticeAdminForm(forms.ModelForm):
    notice_video = forms.CharField(widget=CKEditorUploadingWidget())
    notice_text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Notice
        fields = '__all__'


class NoticeAdmin(admin.ModelAdmin):
    form = NoticeAdminForm


admin.site.register(Notice, NoticeAdmin)
admin.site.register(Category)
admin.site.register(Answer)

