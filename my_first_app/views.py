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
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Task, SubTask, Category
from .pagination import CategoryCursorPagination
from .serializers.subtask import SubTaskCreateSerializer, SubTaskSerializer
from .serializers.task import TaskCreateSerializer, TasksListSerializer, TaskDetailSerializer
from .serializers.category import CategoryCreateSerializer
from .permissions import IsOwnerOrAdminOrReadOnly

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

with_deleted_param = openapi.Parameter(
    "with_deleted", openapi.IN_QUERY, description="Вернуть также мягко удалённые категории (1/true).",
    type=openapi.TYPE_BOOLEAN
)
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    pagination_class = CategoryCursorPagination # т.к. у Category нет смысла сортировать по created_at, делаем отдельно пагинацию

    def get_queryset(self):
        """
        По умолчанию — вернуть все категории, кроме "удалённых".
        ?with_deleted=1 — вернуть все (включая "удалённые").
        """
        qs = Category.objects.all()
        if self.request.query_params.get("with_deleted"):
            qs = Category.all_objects.all()

        return qs

    @swagger_auto_schema(
        operation_summary="Список категорий",
        manual_parameters=[with_deleted_param],
        tags=["Categories"],
        security=JWT_SECURITY,
        responses={200: CategoryCreateSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить категорию",
        tags=["Categories"],
        security=JWT_SECURITY,
        responses={200: CategoryCreateSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать категорию",
        tags=["Categories"],
        request_body=CategoryCreateSerializer,
        security=JWT_SECURITY,
        responses={201: CategoryCreateSerializer(), 400: "Validation error"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить категорию (полностью)",
        tags=["Categories"],
        request_body=CategoryCreateSerializer,
        security=JWT_SECURITY,
        responses={200: CategoryCreateSerializer(), }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить категорию (частично)",
        tags=["Categories"],
        request_body=CategoryCreateSerializer,
        responses={200: CategoryCreateSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="count-tasks")
    def count_tasks(self, request):
        qs = self.queryset.annotate(task_count=Count("tasks")).values("id", "name", "task_count").order_by("name")
        return Response(list(qs), status=status.HTTP_200_OK)

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

class SubTaskListCreateViewGeneric(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SubTask.objects.all().order_by("created_at")
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']  # Поля для поиска
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        return SubTaskCreateSerializer if self.request.method == "POST" else SubTaskSerializer

class SubTaskDetailUpdateDeleteViewGeneric(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
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