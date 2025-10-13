from django.db.models import Count
from django.http import HttpResponse
from rest_framework.decorators import api_view, action
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status as http_status, viewsets, status, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from my_first_app.models import Task
from my_first_app.serializers.subtask import SubTaskCreateSerializer, SubTaskSerializer
from my_first_app.serializers.task import TaskCreateSerializer, TasksListSerializer, TaskDetailSerializer
from my_first_app.permissions import IsOwnerOrAdminOrReadOnly

resp_401 = openapi.Response('Unauthorized')
resp_403 = openapi.Response('Forbidden')
JWT_SECURITY = [{"JWT": []}]


class UserTaskListView(ListAPIView):
    serializer_class = TasksListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    @swagger_auto_schema(
        operation_summary="Мои задачи",
        operation_description="Возвращает список задач, созданных текущим пользователем.",
        tags=["My Tasks"],
        security=JWT_SECURITY,
        responses={200: TasksListSerializer(many=True), 401: resp_401}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

task_filter_params = [
    openapi.Parameter("status", openapi.IN_QUERY, description="Фильтр по статусу", type=openapi.TYPE_STRING),
    openapi.Parameter("deadline_after", openapi.IN_QUERY, description="Дедлайн позже даты (ISO 8601)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
    openapi.Parameter("deadline_before", openapi.IN_QUERY, description="Дедлайн раньше даты (ISO 8601)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
    openapi.Parameter("search", openapi.IN_QUERY, description="Поиск по title/description", type=openapi.TYPE_STRING),
    openapi.Parameter("ordering", openapi.IN_QUERY, description="Сортировка (например, -created_at)", type=openapi.TYPE_STRING),
]

class TaskListCreateViewGeneric(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        return TaskCreateSerializer if self.request.method == "POST" else TasksListSerializer

    @swagger_auto_schema(
        operation_summary="Список задач",
        tags=["Tasks"],
        security=JWT_SECURITY,
        manual_parameters=task_filter_params,
        responses={200: TasksListSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать задачу",
        tags=["Tasks"],
        security=JWT_SECURITY,
        request_body=TaskCreateSerializer,
        responses={201: TaskDetailSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TaskDetailUpdateDeleteViewGeneric(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'pk'

    def get_serializer_class(self):
        return TaskCreateSerializer if self.request.method in {"PUT", "PATCH"} else TasksListSerializer

    @swagger_auto_schema(operation_summary="Получить задачу", tags=["Tasks"], security=JWT_SECURITY)
    def get(self, request, *args, **kwargs): return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Обновить задачу", tags=["Tasks"], security=JWT_SECURITY,
                         request_body=TaskCreateSerializer)
    def put(self, request, *args, **kwargs): return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Частично обновить задачу", tags=["Tasks"], security=JWT_SECURITY,
                         request_body=TaskCreateSerializer)
    def patch(self, request, *args, **kwargs): return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Удалить задачу", tags=["Tasks"], security=JWT_SECURITY)
    def delete(self, request, *args, **kwargs): return super().delete(request, *args, **kwargs)

@api_view(['GET'])
def tasks_statistic_view(request):
    now = timezone.now()
    tasks_total = Task.objects.count()
    tasks_by_status = Task.objects.values('status').annotate(cnt=Count('id')).values_list('status', 'cnt').order_by('status')
    tasks_overdue = Task.objects.filter(deadline__lt=now).exclude(status=http_status.HTTP_200_OK).count()

    return Response({"Total tasks": tasks_total, "Overdue tasks": tasks_overdue, "Tasks by status": dict(tasks_by_status)})
