from django.db import models
from .enums import Status

class Category(models.Model):
    """
    Категория выполнения.
    """
    name = models.CharField(max_length=50, verbose_name="Категория выполнения", unique=True)

    @property
    def list_tasks(self):
        return list(self.tasks.all())

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ('name',)

    def __str__(self):
        return self.name

class Task(models.Model):
    """
    Задача для выполнения.
    """
    title = models.CharField(max_length=100, unique_for_date="created_at", verbose_name="Задача для выполнения")
    description = models.TextField(blank=True, verbose_name="Описание задачи")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW, verbose_name="Статус задачи")
    deadline = models.DateTimeField(verbose_name="Дата и время дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    categories = models.ManyToManyField(Category, related_name="tasks", blank=True)

    class Meta:
        db_table = 'task_manager_task'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
        unique_together = ('title',)

    @property
    def list_categories(self):
        return list(self.categories.all())

    @property
    def list_subtasks(self):
        return list(self.subtasks.all())

    def __str__(self):
        return f'{self.title}'


class SubTask(models.Model):
    """
    Отдельная часть основной задачи (Task).
    """
    title = models.CharField(max_length=100, verbose_name="Название подзадачи")
    description = models.TextField(null=True, blank=True, verbose_name="Описание подзадачи")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW, verbose_name="Статус подзадачи")
    deadline = models.DateTimeField(verbose_name="Дата и время дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE, null=True, verbose_name="Задача")

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'
        ordering = ['created_at']
        unique_together = ('title',)

    def __str__(self):
        return f'{self.title}'