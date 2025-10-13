from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from my_first_app.models import Category
from my_first_app.pagination import CategoryCursorPagination
from my_first_app.serializers.category import CategoryCreateSerializer

JWT_SECURITY = [{"JWT": []}]

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


