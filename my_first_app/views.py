from django.db.models import Count
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status as http_status
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from django_learn.settings import PAGE_SIZE
from my_first_app.models import Task, SubTask
from my_first_app.serializers.subtask import SubTaskCreateSerializer, SubTaskSerializer
from my_first_app.serializers.task import TaskCreateSerializer, TasksListSerializer, TaskDetailSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

"""
Задание 1: Замена представлений для задач (Tasks) на Generic Views
Шаги для выполнения:
    Замените классы представлений для задач на Generic Views:
    Используйте ListCreateAPIView для создания и получения списка задач.
    Используйте RetrieveUpdateDestroyAPIView для получения, обновления и удаления задач.
Реализуйте фильтрацию, поиск и сортировку:
    Реализуйте фильтрацию по полям status и deadline.
    Реализуйте поиск по полям title и description.
    Добавьте сортировку по полю created_at.
"""
class TaskListCreateViewGeneric(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']  # Поля для поиска
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        return TaskCreateSerializer if self.request.method == "POST" else TasksListSerializer

class TaskDetailUpdateDeleteViewGeneric(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'pk'
    # lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        return TaskCreateSerializer if self.request.method in {"PUT", "PATCH"} else TasksListSerializer

"""
Задание 2: Замена представлений для подзадач (SubTasks) на Generic Views
Шаги для выполнения:
    Замените классы представлений для подзадач на Generic Views:
    Используйте ListCreateAPIView для создания и получения списка подзадач.
    Используйте RetrieveUpdateDestroyAPIView для получения, обновления и удаления подзадач.
Реализуйте фильтрацию, поиск и сортировку:
    Реализуйте фильтрацию по полям status и deadline.
    Реализуйте поиск по полям title и description.
    Добавьте сортировку по полю created_at.
"""
class SubTaskListCreateViewGeneric(ListCreateAPIView):
    queryset = SubTask.objects.all()
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
    lookup_field = 'pk'
    # lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        return SubTaskCreateSerializer if self.request.method in {"PUT", "PATCH"} else SubTaskSerializer


# def get_task(pk):
#     try:
#         return Task.objects.get(pk=pk)
#
#     except Task.DoesNotExist:
#         raise NotFound(detail=f'Задача (id={pk}) не найдена')
#
# def get_subtask(pk):
#     try:
#         return SubTask.objects.get(pk=pk)
#
#     except SubTask.DoesNotExist:
#         raise NotFound(detail=f'Подзадача (id={pk}) не найдена')
#
#
# class TaskListCreateView(APIView):
#     def get(self, request, *args, **kwargs):
#         filters = {}
#         week_day = request.query_params.get('week_day', None)
#         if week_day is not None:
#             filters['deadline__week_day'] = week_day
#
#         if filters:
#             tasks = Task.objects.filter(**filters).order_by('-created_at')
#             if tasks.count() == 0:
#                 return Response({"message": f"По вашему запросу {dict(request.query_params)} данные не найдены."}, status=http_status.HTTP_204_NO_CONTENT)
#         else:
#             tasks = Task.objects.all().order_by('-created_at')
#
#         serializer = TaskDetailSerializer(tasks, many=True)
#
#         return Response(serializer.data, status=http_status.HTTP_200_OK)
#
#     def post(self, request, *args, **kwargs):
#         serializer = TaskDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=http_status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
#
#
# class TaskDetailUpdateDeleteView(APIView):
#     def get(self, request, pk):
#         task = get_task(pk)
#         serializer = TaskDetailSerializer(task)
#
#         return Response(serializer.data, status=http_status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         task = get_task(pk)
#         serializer = TaskCreateSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data)
#
#         return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         task = get_task(pk)
#         serializer = TaskDetailSerializer(task, data=request.data, partial=True)  # частичное
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=http_status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         task = get_task(pk)
#         task.delete()
#
#         return Response({"message": f"Deleted Task (id={pk}) success"}, status=http_status.HTTP_204_NO_CONTENT)
#
#
# class SubTaskListCreateView(APIView, PageNumberPagination):
#
#     def get(self, request, *args, **kwargs):
#         filters = {}
#         week_day = request.query_params.get('week_day', None)
#         if week_day is not None and week_day.isdigit():
#             filters['deadline__week_day'] = week_day
#
#         task_name = request.query_params.get('task_name', None)
#         if task_name is not None:
#             filters['task__title__istartswith'] = task_name  # c istartswith, думаю, будет удобнее искать
#
#         status = request.query_params.get('status', None)
#         if status is not None:
#             filters['status__iexact'] = status
#
#         if filters:
#             subtasks = SubTask.objects.filter(**filters).order_by('-created_at')
#             if subtasks.count() == 0:
#                 return Response({"message": f"По запросу {dict(request.query_params)} данные не найдены."},
#                                 status=http_status.HTTP_204_NO_CONTENT)
#         else:
#             subtasks_all = SubTask.objects.all().order_by('-created_at')
#             # делаем пагинацию
#             self.page_size = self.get_page_size(request)
#             subtasks = self.paginate_queryset(subtasks_all, request, view=self)
#
#         serializer = SubTaskSerializer(subtasks, many=True)
#
#         return Response(serializer.data, status=http_status.HTTP_200_OK)
#
#     def get_page_size(self, request):
#         page_size = request.query_params.get('page_size', None)
#         if page_size and page_size.isdigit():
#             return int(page_size)
#         return PAGE_SIZE
#
#     def post(self, request, *args, **kwargs):
#         serializer = SubTaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=http_status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
#
#
# class SubTaskDetailUpdateDeleteView(APIView):
#
#     def get(self, request, pk):
#         subtask = get_subtask(pk)
#         serializer = SubTaskSerializer(subtask)
#
#         return Response(serializer.data, status=http_status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         subtask = get_subtask(pk)
#         serializer = SubTaskCreateSerializer(subtask, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data)
#
#         return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         subtask = get_subtask(pk)
#         serializer = SubTaskSerializer(subtask, data=request.data, partial=True)  # частичное
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=http_status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         subtask = get_subtask(pk)
#         subtask.delete()
#
#         return Response({"message": f"Deleted Subtask (id={pk}) success"}, status=http_status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['POST', 'GET'])
# def tasks_view(request):
#     if request.method == 'GET':
#         tasks = Task.objects.all()
#         serializer = TasksListSerializer(tasks, many=True)
#
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = TaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=http_status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# def task_detail_view(request, pk):
#     try:
#         task = Task.objects.get(pk=pk)
#     except Task.DoesNotExist:
#
#         return Response(status=http_status.HTTP_404_NOT_FOUND)
#
#     serializer = TaskDetailSerializer(task)
#
#     return Response(serializer.data, status=http_status.HTTP_200_OK)
#
#
@api_view(['GET'])
def tasks_statistic_view(request):
    now = timezone.now()
    tasks_total = Task.objects.count()
    tasks_by_status = Task.objects.values('status').annotate(cnt=Count('id')).values_list('status', 'cnt').order_by('status')
    tasks_overdue = Task.objects.filter(deadline__lt=now).exclude(status=http_status.DONE).count()

    return Response({"Total tasks": tasks_total, "Overdue tasks": tasks_overdue, "Tasks by status": dict(tasks_by_status)})

def hello(request, name):
    return HttpResponse(f'<h1>Hello, {name}</h1>')