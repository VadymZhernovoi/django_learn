from rest_framework import serializers
from my_first_app.models import Category
"""
Задание 2: Реализация мягкого удаления категорий
Шаги для выполнения:
1. Добавьте два новых поля в вашу модель Category, если таких ещё не было.
    В модели Category добавьте поля is_deleted(Boolean, default False) и deleted_at(DateTime, null=true)
    Переопределите метод удаления, чтобы он обновлял новые поля к соответствующим значениям: is_deleted=True и дата и время на момент “удаления” записи
2. Переопределите менеджера модели Category
    В менеджере модели переопределите метод get_queryset(), чтобы он по умолчанию выдавал только те записи, которые не “удалены” из базы.
"""

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value: str):
        """
        Проверяет, чтобы название категории не было пустым и не повторялось в БД
        :param value:
        :return:
        """
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Название категории не может быть пустым.")

        qs = Category.objects.filter(name__iexact=value, is_deleted=False)

        if self.instance:  # исключаем из проверки саму себя
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")

        return value


    def update(self, instance, validated_data):
        """
        Дополнительно проверяем на уникальность названия категории
        :param instance:
        :param validated_data:
        :return:
        """
        name = validated_data.pop('name', None)
        name = (name or "").strip() # убираем лишние пробелы
        # регистронезависимо ищем категорию с таким названием, исключая из поиска саму себя
        if Category.objects.filter(name__iexact=name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({"name": "Категория с таким названием уже существует."})

        instance.name = name
        instance.save(update_fields=["name"])

        return instance