from django.utils import timezone
from rest_framework import serializers
from my_first_app.models import Task, Category
from my_first_app.serializers.subtask import SubTaskSerializer

"""
Создайте TaskCreateSerializer и добавьте валидацию для поля deadline, 
чтобы дата не могла быть в прошлом. Если дата в прошлом, возвращайте ошибку валидации.
Шаги для выполнения:
    Определите TaskCreateSerializer в файле serializers.py.
    Переопределите метод validate_deadline для проверки даты.
"""
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "deadline")

    def validate_deadline(self, value):
        """
        Дополнительно проверяет, чтобы дата deadline не могла быть в прошлом
        :param value:
        :return:
        """
        now = timezone.now()
        if value <= now:
            raise serializers.ValidationError("Deadline не может быть в прошлом.")

        return value

class TasksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "status", "deadline", "created_at")
"""
Создайте сериализатор для TaskDetailSerializer, 
который включает вложенный сериализатор для полного отображения связанных подзадач (SubTask). 
Сериализатор должен показывать все подзадачи, связанные с данной задачей.
Шаги для выполнения:
    Определите TaskDetailSerializer в файле serializers.py.
    Вложите SubTaskSerializer внутрь TaskDetailSerializer.
"""
class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
            "updated_at",
            "subtasks",
            "categories",
        ]
        read_only_fields = ("id", "created_at", "updated_at", "subtasks", "categories")

