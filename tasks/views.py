from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # Work with database
    # transform data
    # Data pass
    # Return http / json response
    return HttpResponse("Welcome to the task management system.")

def manager_dashboard(request):
    return render(request,"dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request,"dashboard/user-dashboard.html")