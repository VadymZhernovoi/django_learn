from typing import Callable
from django.http import HttpRequest, HttpResponse

def log_auth_header(get_response: Callable) -> Callable:
    """
    Временный middleware: печатает значение HTTP_AUTHORIZATION для каждого запроса.
    УДАЛИТЕ после отладки — в логах будет токен!
    """
    def middleware(request: HttpRequest) -> HttpResponse:
        # В dev (runserver) print попадёт в консоль
        print("HTTP_AUTHORIZATION:", request.META.get("HTTP_AUTHORIZATION"))
        return get_response(request)
    return middleware