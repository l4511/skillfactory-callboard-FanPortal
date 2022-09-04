from django.urls import path
from .views import NoticeList, NoticeDetailView, NoticeCreateView, NoticeDeleteView, NoticeUpdateView, Confirm, Cancel, AccountView

urlpatterns = [
    path('', NoticeList.as_view()),
    path('<int:pk>/', NoticeDetailView.as_view(), name='notice_detail'),
    path('create/', NoticeCreateView.as_view(), name='notice_create'),
    path('<int:pk>/delete/', NoticeDeleteView.as_view(), name='notice_delete'),
    path('<int:pk>/update/', NoticeUpdateView.as_view(), name='notice_update'),
    path('confirm/<int:pk>/', Confirm.as_view(), name='answer_confirm'),
    path('cancel/<int:pk>/', Cancel.as_view(), name='answer_cancel'),
    path('account/', AccountView.as_view(), name='account'),
    ]
