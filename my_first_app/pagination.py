from rest_framework.pagination import CursorPagination


class DefaultCursorPagination(CursorPagination):
    page_size = 6
    cursor_query_param = 'cursor'
    ordering = "created_at"

class CategoryCursorPagination(CursorPagination):
    page_size = 6
    cursor_query_param = 'cursor'
    ordering = '-name'