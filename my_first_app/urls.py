from django.urls import path, include
from rest_framework import routers

from my_first_app.views import (CategoryViewSet, TaskDetailUpdateDeleteViewGeneric, TaskListCreateViewGeneric,
                                SubTaskListCreateViewGeneric, SubTaskDetailUpdateDeleteViewGeneric,
                                tasks_statistic_view)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
urlpatterns = [
    path('tasks/', TaskListCreateViewGeneric.as_view(), name="tasks-list-create"),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteViewGeneric.as_view(), name="task-detail-update"),
    path('subtasks/', SubTaskListCreateViewGeneric.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteViewGeneric.as_view(), name='subtask-detail-update'),
    path('tasks/stats/', tasks_statistic_view, name='tasks-statistic'),
    path('' , include(router.urls)),
]

