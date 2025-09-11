from django.contrib import admin
from my_first_app.models import Task, SubTask, Category, Status
from django.utils.text import Truncator

# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    verbose_name = 'Задача'
    verbose_name_plural = "Задачи"
    list_display = ('short_title', 'status', 'deadline', 'created_at', 'list_subtasks', 'list_categories')
    list_editable = ('status', 'deadline')
    search_fields = ('title',)
    list_filter = ('title', 'status', 'deadline')
    ordering = ('-deadline', 'title')
    readonly_fields = ('created_at',)
    fields = ('title', 'status', 'deadline', 'description', 'categories', 'created_at', )
    list_per_page = 10

    @admin.display(description='Задача', ordering='title')
    def short_title(self, obj):
        # short = obj.title
        # return short if len(short) <= 10 else short[:10] + "…"
        return Truncator(obj.title).chars(10)

    @admin.display(description='Подзадачи ')
    def list_subtasks(self, obj):
        return obj.list_subtasks

    @admin.display(description='Категории')
    def list_categories(self, obj):
        return obj.list_categories

def action_set_status(status_value, description):

    def action(modeladmin, request, queryset):
        queryset.update(status=status_value)

    action.short_description = description
    action.__name__ = f"status_{status_value}".replace(' ', '_')
    return action

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    verbose_name = 'Подзадача'
    verbose_name_plural = "Подзадачи"
    list_display = ('title', 'task', 'status', 'deadline')
    list_editable = ('status', 'deadline')
    search_fields = ('title',)
    list_filter = ('title', 'status', 'deadline')
    ordering = ('-deadline', 'task', 'title')
    fields = ('title', 'task', 'status', 'deadline', 'description')
    list_per_page = 10

    actions = [
        action_set_status(f"{value}", f"Установить статус '{label}'")
        for value, label in Status.choices
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    verbose_name = 'Категория'
    verbose_name_plural = "Категории"
    list_display = ('name','list_tasks')
    search_fields = ('name',)
    list_filter = ('name',)
    list_per_page = 10

    @admin.display(description='Задачи')
    def list_tasks(self, obj):
        return obj.list_tasks
