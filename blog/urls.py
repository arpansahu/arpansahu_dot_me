from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('post/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('post/<slug:post_slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:post_slug>/like/', views.toggle_post_like, name='toggle_post_like'),
    path('comment/<int:comment_id>/like/', views.toggle_comment_like, name='toggle_comment_like'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
