from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('<int:comment_id>/like/', views.toggle_like_comment, name='toggle_like'),
    path('<int:comment_id>/history/', views.get_edit_history, name='edit_history'),
]
