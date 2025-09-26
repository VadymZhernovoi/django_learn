import django
from django.utils import timezone
from datetime import timedelta
from my_first_app.enums import Status
from django.utils import timezone
from django.db.models import F

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_library.settings')
django.setup()

from my_first_app.models import Task, SubTask
subtasks = (
    {
    "title": "Gather information",
    "description": "Find necessary information for the presentation",
    "status": Status.NEW,
    "deadline_day": 2
    },
    {
    "title": "Create slides",
    "description": "Create presentation slides",
    "status": Status.NEW,
    "deadline_day": 1
    },
    {
    "title": "Subtask with status 'Done' and deadline_day -3",
    "description": "fdcefcv ervervf e ",
    "status": Status.DONE,
    "deadline_day": 1
    }
)
"""
Создание записей:
Task:
    title: "Prepare presentation".
    description: "Prepare materials and slides for the presentation".
    status: "New".
    deadline: Today's date + 3 days.

SubTasks для "Prepare presentation":
    title: "Gather information".
    description: "Find necessary information for the presentation".
    status: "New".
    deadline: Today's date + 2 days.

    title: "Create slides".
    description: "Create presentation slides".
    status: "New".
    deadline: Today's date + 1 day.
"""
def create_task():
    task = Task.objects.create(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status=Status.NEW,
        deadline=timezone.now() + timedelta(days=3),)
    print(f'Created task "{task.title}", status: {task.status}, deadline: {task.deadline}, deadline: {task.deadline}')
    return task


def create_subtask(task, subtask):
    print(task, subtask)
    subtask = SubTask.objects.create(
        task=task,
        title=subtask["title"],
        description=subtask["description"],
        status=subtask["status"],
        deadline=timezone.now() + timedelta(days=subtask["deadline_day"]),
    )
    print(f'Created subtask "{subtask.title}", task "{subtask.task.title}", status: {subtask.status}, deadline: {subtask.deadline}')
    return subtask

"""
Чтение записей:
Tasks со статусом "New":
    Вывести все задачи, у которых статус "New".
SubTasks с просроченным статусом "Done":
    Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
"""
def list_tasks_new():
    tasks = Task.objects.filter(status=Status.NEW)
    if tasks:
        print('Tasks with the status “New”.')
        for task in tasks:
            print(task.title, task.status, task.deadline, task.description)
    else:
        print('Tasks that do not have the “New” status.')

def list_subtasks_done():
    subtasks = SubTask.objects.filter(status=Status.DONE, deadline__lt=timezone.now())
    if subtasks:
        print('Subtasks with the status “Done” but whose deadline has passed.')
        for subtask in subtasks:
            print(subtask.title, subtask.status, subtask.deadline, subtask.description)
    else:
        print('Subtasks with the status “Done” and an expired deadline are missing.')

"""
Изменение записей:
Измените статус "Prepare presentation" на "In progress".
Измените срок выполнения для "Gather information" на два дня назад.
Измените описание для "Create slides" на "Create and format presentation slides".
"""
def change_task():
    Task.objects.filter(title="Prepare presentation").update(status=Status.IN_PROGRESS)
    task = Task.objects.get(title="Prepare presentation")
    print(f'Updated task "{task.title}" for status to {Status.IN_PROGRESS}.')

def change_subtasks_1_2(subtask_1, subtask_2):
    deadline_old = subtask_1.deadline
    SubTask.objects.filter(title=subtask_1.title).update(deadline=F('deadline') - timedelta(days=2))
    subtask_up = SubTask.objects.get(title=subtask_1.title)
    print(f'Updated subtask "{subtask_1.title}" - older deadline: {deadline_old}, new deadline: {subtask_up.deadline}.')

    description_old = subtask_2.description
    SubTask.objects.filter(title=subtask_2.title).update(description="modified: Create and format presentation slides")
    subtask_up = SubTask.objects.get(title=subtask_2.title)
    print(f'Updated subtask "{subtask_2.title}" - older description: {description_old}, new description: {subtask_up.description}."')

"""
Удаление записей:
Удалите задачу "Prepare presentation" и все ее подзадачи.
"""
def delete_task_with_subtasks(task):
    deleted, _ = task.delete()
    if deleted:
        print(f'Deleted {deleted} records.')
    else:
        print(f'Not deleted records.')


