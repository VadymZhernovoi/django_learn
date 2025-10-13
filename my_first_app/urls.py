from django.urls import path, include
from rest_framework import routers

from my_first_app.views.category import CategoryViewSet
from my_first_app.views.task import TaskDetailUpdateDeleteViewGeneric, TaskListCreateViewGeneric, UserTaskListView, tasks_statistic_view
from my_first_app.views.subtask import SubTaskListCreateViewGeneric, SubTaskDetailUpdateDeleteViewGeneric
from my_first_app.views.user import RegisterView, LoginView, LogoutView

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
urlpatterns = [
    path("user/register/", RegisterView.as_view(), name="register"),
    path("user/login/", LoginView.as_view(), name="login"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
    path('user-tasks/', UserTaskListView.as_view(), name="user-tasks-list"),
    path('tasks/', TaskListCreateViewGeneric.as_view(), name="tasks-list-create"),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteViewGeneric.as_view(), name="task-detail-update"),
    path('subtasks/', SubTaskListCreateViewGeneric.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteViewGeneric.as_view(), name='subtask-detail-update'),
    path('tasks/stats/', tasks_statistic_view, name='tasks-statistic'),
    path('' , include(router.urls)),
]

