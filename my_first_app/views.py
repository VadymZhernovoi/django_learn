from django.db.models import Count
from django.http import HttpResponse
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import api_view, action
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status as http_status, viewsets, status, generics, mixins
from django.utils import timezone
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

from my_first_app.models import Task, SubTask, Category
from my_first_app.pagination import DefaultCursorPagination, CategoryCursorPagination
from my_first_app.serializers.subtask import SubTaskCreateSerializer, SubTaskSerializer
from my_first_app.serializers.task import TaskCreateSerializer, TasksListSerializer, TaskDetailSerializer
from my_first_app.serializers.category import CategoryCreateSerializer
"""
Задание 1: Реализация CRUD для категорий с использованием ModelViewSet
Шаги для выполнения:
    Создайте CategoryViewSet, используя ModelViewSet для CRUD операций.
    Добавьте маршрут для CategoryViewSet.
    Добавьте кастомный метод count_tasks используя декоратор @action для подсчета количества задач, связанных с каждой категорией.
"""

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    pagination_class = CategoryCursorPagination # т.к. у Category нет смысла сортировать по created_at, делаем отдельно пагинацию
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        """
        По умолчанию — вернуть все категории, кроме "удалённых".
        ?with_deleted=1 — вернуть все (включая "удалённые").
        """
        qs = Category.objects.all()
        if self.request.query_params.get("with_deleted"): # потренироваться
            qs = Category.all_objects.all()

        return qs

    @action(detail=False, methods=["get"], url_path="count-tasks")
    def count_tasks(self, request):
        qs = self.queryset.annotate(task_count=Count("tasks")).values("id", "name", "task_count").order_by("name")

        return Response(list(qs), status=status.HTTP_200_OK)


class TaskListCreateViewGeneric(generics.ListCreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


    def get_serializer_class(self):
        return TaskCreateSerializer if self.request.method == "POST" else TasksListSerializer

class TaskDetailUpdateDeleteViewGeneric(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return TaskCreateSerializer if self.request.method in {"PUT", "PATCH"} else TasksListSerializer

class SubTaskListCreateViewGeneric(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = SubTask.objects.all().order_by("created_at")
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']  # Поля для поиска
    ordering_fields = ['created_at']


    def get_serializer_class(self):
        return SubTaskCreateSerializer if self.request.method == "POST" else SubTaskSerializer

class SubTaskDetailUpdateDeleteViewGeneric(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'
    # lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        return SubTaskCreateSerializer if self.request.method in {"PUT", "PATCH"} else SubTaskSerializer


@api_view(['GET'])
def tasks_statistic_view(request):
    now = timezone.now()
    tasks_total = Task.objects.count()
    tasks_by_status = Task.objects.values('status').annotate(cnt=Count('id')).values_list('status', 'cnt').order_by('status')
    tasks_overdue = Task.objects.filter(deadline__lt=now).exclude(status=http_status.HTTP_200_OK).count()

    return Response({"Total tasks": tasks_total, "Overdue tasks": tasks_overdue, "Tasks by status": dict(tasks_by_status)})

def hello(request, name):
    return HttpResponse(f'<h1>Hello, {name}</h1>')