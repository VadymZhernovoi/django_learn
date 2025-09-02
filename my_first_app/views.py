from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_first_app(request):
    return HttpResponse("<h1>Hello, Vadym</h1>")