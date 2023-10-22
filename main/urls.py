from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('entries/<int:post_id>/', views.entries, name='entries'),
    path('create_entry/<int:post_id>/', views.create_entry, name='create_entry'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('update_entry/<int:entry_id>/', views.update_entry, name='update_entry')
]
