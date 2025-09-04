from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # Work with database
    # transform data
    # Data pass
    # Return http / json response
    return HttpResponse("Welcome to the task management system.")

def contact(request):
    return HttpResponse("<h1 style = 'color:blue'>This is contact page.</h1>")

def show_task(request):
    return HttpResponse("This is task page.")

def show_specific_task(request,id):
    print("id",id)
    print("id type", type(id))
    return HttpResponse("This is specific task page.")