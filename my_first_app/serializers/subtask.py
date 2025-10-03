from django.utils import timezone
from rest_framework import serializers
from my_first_app.models import SubTask, Task


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = SubTask
        fields = ["id", "title", "description", "status", "deadline", "task", "created_at", "owner"]
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

class SubTaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = SubTask
        fields = ["id", "title", "description", "status", "deadline", "task", "created_at", "updated_at", "owner"]
        read_only_fields = ('owner',)

