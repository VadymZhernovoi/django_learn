from django.db.models import Count
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from my_first_app.models import Task, SubTask
from my_first_app.serializers.subtask import SubTaskCreateSerializer, SubTaskSerializer
from my_first_app.serializers.task import TaskCreateSerializer, TasksListSerializer, TaskDetailSerializer
from my_first_app.enums import Status


def hello(request, name):

    return HttpResponse(f'<h1>Hello, {name}</h1>')

"""
Создайте классы представлений для работы с подзадачами (SubTasks), 
включая создание, получение, обновление и удаление подзадач. 
Используйте классы представлений (APIView) для реализации этого функционала.
Шаги для выполнения:
    Создайте классы представлений для создания и получения списка подзадач (SubTaskListCreateView).
    Создайте классы представлений для получения, обновления и удаления подзадач (SubTaskDetailUpdateDeleteView).
    Добавьте маршруты в файле urls.py, чтобы использовать эти классы.
"""
def get_task(pk):
    try:
        return Task.objects.get(pk=pk)

    except Task.DoesNotExist:
        raise NotFound(detail=f'Задача (id={pk}) не найдена')

def get_subtask(pk):
    try:
        return SubTask.objects.get(pk=pk)

    except SubTask.DoesNotExist:
        raise NotFound(detail=f'Подзадача (id={pk}) не найдена')

class SubTaskListCreateView(APIView):

    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):

    def get(self, request, pk):
        subtask = get_subtask(pk)
        serializer = SubTaskSerializer(subtask)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subtask = get_subtask(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        subtask = get_subtask(pk)
        serializer = SubTaskSerializer(subtask, data=request.data, partial=True)  # частичное
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = get_subtask(pk)
        subtask.delete()

        return Response({"message": f"Deleted Subtask (id={pk}) success"}, status=status.HTTP_204_NO_CONTENT)

class TaskListCreateView(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskDetailSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TaskDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailUpdateDeleteView(APIView):

    def get(self, request, pk):
        task = get_task(pk)
        serializer = TaskDetailSerializer(task)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = get_task(pk)
        serializer = TaskCreateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = get_task(pk)
        serializer = TaskDetailSerializer(task, data=request.data, partial=True)  # частичное
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_task(pk)
        task.delete()

        return Response({"message": f"Deleted Task (id={pk}) success"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'GET'])
def tasks_view(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TasksListSerializer(tasks, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_detail_view(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailSerializer(task)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def tasks_statistic_view(request):
    now = timezone.now()
    tasks_total = Task.objects.count()
    tasks_by_status = Task.objects.values('status').annotate(cnt=Count('id')).values_list('status', 'cnt').order_by('status')
    tasks_overdue = Task.objects.filter(deadline__lt=now).exclude(status=Status.DONE).count()

    return Response({"Total tasks": tasks_total, "Overdue tasks": tasks_overdue, "Tasks by status": dict(tasks_by_status)})

