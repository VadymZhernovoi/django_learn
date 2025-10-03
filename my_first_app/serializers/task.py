from django.utils import timezone
from rest_framework import serializers
from my_first_app.models import Task, Category
from my_first_app.serializers.subtask import SubTaskSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "deadline", "created_at", 'owner')
        read_only_fields = ('owner',)

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
        fields = ("id", "title", "status", "deadline", "created_at", 'owner')
        read_only_fields = ('owner',)


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
            'owner',
        ]
        read_only_fields = ("id", "created_at", "updated_at", "subtasks", "categories", 'owner',)


