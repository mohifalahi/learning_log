from django.urls import path
from . import views

app_name = 'logger'

urlpatterns = [
    path('', views.home, name='home'),
    path('topics/', views.topic, name='topic'),
    path('add_topic/', views.add_topic, name='add_topic'),
    path('topics/<int:topic_id>/', views.entry, name='entry'),
    path('add_entry/<int:topic_id>/', views.add_entry, name='add_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry')
]