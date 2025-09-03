from django.db import models

STATUS_CHOICES = [
    ('New', 'New'),
    ('In progress', 'In progress'),
    ('Pending', 'Pending'),
    ('Blocked', 'Blocked'),
    ('Done', 'Done')
]

class Category(models.Model):
    """
    Категория выполнения.
    """
    name = models.CharField(max_length=50, verbose_name="Категория выполнения", unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    """
    Задача для выполнения.
    """
    title = models.CharField(max_length=100, unique_for_date="created_at", verbose_name="Задача для выполнения")
    description = models.TextField(blank=True, verbose_name="Описание задачи")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], verbose_name="Статус задачи")
    deadline = models.DateTimeField(verbose_name="Дата и время дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    categories = models.ManyToManyField(Category, related_name="tasks", blank=True)

    def __str__(self):
        return f'{self.description}, {self.status}, {self.deadline}'


class SubTask(models.Model):
    """
    Отдельная часть основной задачи (Task).
    """
    title = models.CharField(max_length=100, verbose_name="Название подзадачи")
    description = models.TextField(null=True, blank=True, verbose_name="Описание подзадачи")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], verbose_name="Статус подзадачи")
    deadline = models.DateTimeField(verbose_name="Дата и время дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.title}, task: {self.task}, {self.status}, {self.deadline}'
