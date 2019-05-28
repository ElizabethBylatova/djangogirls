from django.urls import path

from . import views

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostNew.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.DetailView.as_view(), name='post_edit'),
]
