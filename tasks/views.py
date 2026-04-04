from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Task, Project
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView

# Create your views here.
def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(lambda u: is_manager(u) or is_admin(u), login_url='no-permission')
def manager_dashboard(request):
    type = request.GET.get('type','all') 
    
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id',filter=Q(status='COMPLETED')),
        in_progress=Count('id',filter=Q(status='IN_PROGRESS')),
        pending=Count('id',filter=Q(status='PENDING'))
    )

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()

    context = {
        "tasks": tasks,
        "counts": counts
    }    
    return render(request,"dashboard/manager-dashboard.html",context)

@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request,"dashboard/user-dashboard.html")

@login_required
@permission_required("tasks.add_task", login_url='no-permission')
def create_task(request):
    #employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request,"Task Created Successfully")
            return redirect('create-task')
            
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

    context = {"task_form":task_form, "task_detail_form":task_detail_form}
    return render(request, "task_form.html", context)

""" Class Based View Example for Task Create"""

# variable for list of decorators
""" 
create_decorators = [login_required, permission_required(
    "tasks.add_task", login_url='no-permission')]
@method_decorator(create_decorators, name="dispatch") 

"""
class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    """ For Creating task"""

    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name = 'task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get(
            'task_detail_form', TaskDetailModelForm())
        return context

    def get(self, request, *args, **kwargs):
        # task_form = TaskModelForm()  # For GET
        # task_detail_form = TaskDetailModelForm()
        # context = {"task_form": task_form,
        #            "task_detail_form": task_detail_form}
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            #return redirect('create-task')
            context = self.get_context_data(
                task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)

@login_required
@permission_required("tasks.view_task", login_url='no-permission')
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

    # prefetch_related(ManytoMany, reverse Foreignkey)
    tasks4 = Task.objects.prefetch_related("assigned_to").all()

    # number of task 
    task_count = Task.objects.aggregate(num_task=Count('id'))

    # count the number of task in a specific project
    project_task_count = Project.objects.annotate(num_task=Count('task')).order_by('num_task')

    return render(request,"show_task.html",{"tasks":tasks,"first_task":task_first, "tasks2":tasks2,"tasks3":tasks3,"tasks4":tasks4, "task_count":task_count, "project_task_count":project_task_count})


view_project_decorators = [login_required]

@method_decorator(view_project_decorators, name='dispatch')
class ViewProject(ListView):
    model = Project  
    context_object_name = 'projects'  
    template_name = 'show_task.html' 

    def get_queryset(self):
        queryset = Project.objects.annotate(
            num_task=Count('task')  
        ).order_by('num_task')  
        return queryset

@login_required
@permission_required("tasks.change_task", login_url='no-permission')
def update_task(request,id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":
        task_form = TaskModelForm(request.POST,instance=task)
        task_detail_form = TaskDetailModelForm(request.POST,instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request,"Task Updated Successfully")
            return redirect('update-task',id)
            

    context = {"task_form":task_form, "task_detail_form":task_detail_form}
    return render(request, "task_form.html", context)

class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        print(context)
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(
                instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', self.object.id)
        return redirect('update-task', self.object.id)


@login_required
@permission_required("tasks.delete_task", login_url='no-permission')
def delete_task(request,id):

    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task Deleted Successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request, "Something went wrong")
        return redirect('manager-dashboard')
    

@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES

    if request.method == 'POST':
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)
    
    return render(request, 'task_details.html', {"task": task, 'status_choices':status_choices})

class TaskDetail(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # {"task": task}
        # {"task": task, 'status_choices': status_choices}
        context['status_choices'] = Task.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)

@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    return redirect('no-permission')