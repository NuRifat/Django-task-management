from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task


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

def test(request):
    context = {
        "names" : ["Rahim","Sakib","John"]
    }
    return render(request,"test.html",context)


def create_task(request):
    #employees = Employee.objects.all()
    form = TaskModelForm()

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """ For Model Form Data """
            form.save()

            return render(request, 'task_form.html',{"form":form, "message":"task added successfully"})
            
            """ For Django Form Data """
            # data = form.cleaned_data
            # project = data.get('project')
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # status = data.get('status')
            # is_completed = data.get('is_completed')
            # assigned_to = data.get('assigned_to')

            # task = Task.objects.create(
            #     project=project, title=title, description=description, due_date=due_date, status=status, is_completed=is_completed
            # )

            # #Assign employee to tasks
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            #return HttpResponse("Task added successfully")

    context = {"form":form}
    return render(request, "task_form.html", context)

def view_task(request):
    # retrive all data from task model
    #tasks = Task.objects.all()
    # fetch the 1st task
    task_first = Task.objects.first()

    # Show the task that are completed
    tasks = Task.objects.filter(status="COMPLETED")

    #select_related(Foreign,OnetoOne)
    tasks2 = Task.objects.select_related('details').all()#for OneToOne
    tasks3 = Task.objects.select_related('project').all()#foreign_key

    #prefetch_related(ManytoMany, reverse Foreignkey)
    tasks4 = Task.objects.prefetch_related("assigned_to").all()

    return render(request,"show_task.html",{"tasks":tasks,"first_task":task_first, "tasks2":tasks2,"tasks3":tasks3,"tasks4":tasks4})