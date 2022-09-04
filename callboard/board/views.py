from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from .models import Notice, Answer
from .filters import NoticeFilter, AccountFilter
from .forms import NoticeForm, AnswerForm
from sign.models import UserCode
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django_filters.views import FilterMixin


def check_valid(self):
    print('post-test')
    if self.request.user.is_authenticated:
        if not UserCode.objects.filter(user_id=self.request.user).values('valid')[0]['valid']:
            print('YeS!!')
            self.request.user.delete()
    return redirect('/notice/')


class NoticeList(ListView):
    model = Notice
    template_name = 'notices.html'
    context_object_name = 'notices'
    queryset = Notice.objects.order_by('-notice_time_create')
    paginate_by = 1

    def get_initial(self):
        initial = super().get_initial()
        initial['notice_user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NoticeFilter(self.request.GET, queryset=self.get_queryset())
        check_valid(self)
        return context


class NoticeDetailView(FormMixin, DetailView):
    model = Notice
    template_name = 'notice_detail.html'
    context_object_name = 'notice'
    form_class = AnswerForm
    queryset = Notice.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        pk = self.kwargs.get('pk')
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form, **kwargs):
        try:
            self.object = form.save(commit=False)
            self.object.answer_user = self.request.user
            self.object.answer_post = self.get_object()
            self.object.save()
            return super().form_valid(form)
        except IntegrityError:
            return redirect('/notice/')

    def get_success_url(self, **kwargs):
        check_valid(self)
        return reverse_lazy('notice_detail', kwargs={'pk': self.get_object().id})


class NoticeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'notice_create.html'
    form_class = NoticeForm

    def get_initial(self):
        initial = super().get_initial()
        initial['notice_user'] = self.request.user
        check_valid(self)
        return initial

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/notice/')


class NoticeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'notice_create.html'
    form_class = NoticeForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Notice.objects.get(pk=id)


class NoticeDeleteView(DeleteView):
    template_name = 'notice_delete.html'
    permission_required = ('board.delete_notice',)
    queryset = Notice.objects.all()
    context_object_name = 'notice'
    success_url = '/notice/'


class AccountView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'account.html'
    context_object_name = 'notices'
    queryset = Answer.objects.order_by('-answer_time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AccountFilter(self.request.GET, queryset=self.get_queryset())
        check_valid(self)
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['answer_user'] = self.request.user
        return initial


class Confirm(UpdateView):
    model = Answer
    template_name = 'confirm.html'
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        check_valid(self)
        context = super().get_context_data(**kwargs)
        context['message'] = 'Вы приняли комментарий'
        id = self.kwargs.get('pk')
        Answer.objects.filter(pk=id).update(answer_confirm=True)
        user = self.object.answer_user
        send_mail(
            subject='Ваш комментарий одобрили!',
            message=f'Пользователь принял ваш комментарий.',
            from_email='alexgoldm1991@yandex.ru',
            recipient_list=[User.objects.filter(username=user).values("email")[0]['email']]
        )
        return context


class Cancel(UpdateView):
    model = Answer
    template_name = 'confirm.html'
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        check_valid(self)
        context = super().get_context_data(**kwargs)
        context['message'] = 'Вы отменили отклик!'
        id = self.kwargs.get('pk')
        Answer.objects.filter(pk=id).update(answer_confirm=False)

        return context
