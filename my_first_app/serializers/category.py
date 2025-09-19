from rest_framework import serializers
from my_first_app.models import Category
"""
Создайте сериализатор для категории CategoryCreateSerializer, 
переопределив методы create и update для проверки уникальности названия категории. 
Если категория с таким названием уже существует, возвращайте ошибку валидации.
Шаги для выполнения:
    Определите CategoryCreateSerializer в файле serializers.py.
    Переопределите метод create для проверки уникальности названия категории.
    Переопределите метод update для аналогичной проверки при обновлении.
"""
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_title(self, value: str):
        """
        Дополнительно проверяет, чтобы название категории не было пустым
        :param value:
        :return:
        """
        value = (value or "").strip() # убираем лишние пробелы
        if not value:
            raise serializers.ValidationError("Название категории не может быть пустым.")

        return value

    def create(self, validated_data):
        """
        Дополнительно проверяем на уникальность названия категории.
        :param validated_data:
        :return:
        """
        title = validated_data.pop('title', [])
        # регистронезависимо ищем категорию с таким названием
        if Category.objects.filter(title__iexact=title).exists():
            raise serializers.ValidationError({"title": "Категория с таким названием уже существует."})

        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Дополнительно проверяем на уникальность названия категории
        :param instance:
        :param validated_data:
        :return:
        """
        title = validated_data.pop('title', None)
        title = (title or "").strip() # убираем лишние пробелы
        # регистронезависимо ищем категорию с таким названием, исключая из поиска саму себя
        if Category.objects.filter(title__iexact=title).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({"title": "Категория с таким названием уже существует."})

        instance.title = title
        instance.save(update_fields=["title"])

        return instance