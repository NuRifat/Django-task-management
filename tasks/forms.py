from django import forms
from tasks.models import Project, Task

class TaskForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label="Select Project")
    title = forms.CharField(max_length=250,label="Task Title")
    description = forms.CharField(widget=forms.Textarea,label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES, label="Status")
    is_completed = forms.BooleanField(required=False, label="Completed?")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[])

    def __init__(self,*args, **kwargs):
        employees = kwargs.pop("employees",[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id,emp.name) for emp in employees]