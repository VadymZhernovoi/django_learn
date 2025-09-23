from django.urls import path
from rest_framework import routers

from my_first_app.views import (TaskDetailUpdateDeleteViewGeneric, TaskListCreateViewGeneric,
                                SubTaskListCreateViewGeneric, SubTaskDetailUpdateDeleteViewGeneric,
                                hello, tasks_statistic_view)

# router = routers.DefaultRouter()
# router.register(r'authors', books_views.AuthorViewSet, basename='authors')
urlpatterns = [
    path('<name>', hello, name='hello'),
    path('api/v1/task/<int:pk>', TaskDetailUpdateDeleteViewGeneric.as_view(), name="task-detail-update"),
    # path('api/v1/task/<int:pk>', TaskDetailUpdateDeleteView.as_view(), name="task-detail-update"),
    path('api/v1/tasks', TaskListCreateViewGeneric.as_view(), name="tasks-list-create"),
    # path('api/v1/tasks', TaskListCreateView.as_view(), name="tasks-list-create"),
    path('api/v1/subtasks', SubTaskListCreateViewGeneric.as_view(), name='subtask-list-create'),
    # path('api/v1/subtasks', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('api/v1/subtask/<int:pk>', SubTaskDetailUpdateDeleteViewGeneric.as_view(), name='subtask-detail-update'),
    # path('api/v1/subtask/<int:pk>', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update'),
    path("api/v1/tasks/stats", tasks_statistic_view, name="tasks-statistic"),
]

