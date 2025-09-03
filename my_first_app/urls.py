from django.urls import path
from my_first_app.views import hello

urlpatterns = [
    path('<name>', hello, name='hello'),
]