from django.contrib import admin
from my_first_app.models import Task, SubTask, Category

# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    verbose_name = 'Задача'
    verbose_name_plural = "Задачи"
    list_display = ('title', 'status', 'deadline', 'created_at')
    list_editable = ('status', 'deadline')
    search_fields = ('title',)
    list_filter = ('title', 'status', 'deadline')
    ordering = ('-deadline', 'title')
    readonly_fields = ('created_at',)
    fields = ('title', 'status', 'deadline', 'description', 'categories', 'created_at', )
    list_per_page = 10


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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    verbose_name = 'Категория'
    verbose_name_plural = "Категории"
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_per_page = 10
