from django.urls import path
from my_first_app.views import my_first_app

urlpatterns = [
    path('', my_first_app, name='hello'),
]