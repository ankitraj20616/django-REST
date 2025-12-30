from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def students(request: HttpRequest):
    return render(request, "students.html")