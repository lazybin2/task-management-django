from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
 
    return HttpResponse('<h1>Task Management</h1>')

def contact(request):
    return HttpResponse("<h1 style='color: red'>Contact Page</h1>")

def show_task(request):
    return HttpResponse("<h1 style='color: green'>Show Task Page</h1>")