from django.urls import path
from . import views

app_name='task'
urlpatterns = [
    path('api/task_creation/', views.TaskCreationView.as_view() , name="task_creation"),

]
