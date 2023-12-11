from django.urls import path
from . import views

app_name = "learning_logs"
urlpatterns = [
    path('', views.index, name='home'),
    path("topics/", views.topics, name="topics"),
    path("topics/<int:topic_id>/", views.topic_entries, name="topic"),
    path("topics/add-new-topic/", views.add_new_topic, name="add_new_topic"),
    path("add_new_entry/<int:topic_id>/", views.add_new_entry, name="add_new_entry"),
    path("edit_entry/<int:entry_id>/", views.edit_entry, name='edit_entry'),
]
