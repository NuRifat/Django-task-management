from django import forms
from tasks.models import Project, Task

# Django Form:
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

# Django Model Form:
class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        #fields = '__all__' #to bring all the fields from Task
        fields = ['title','description','due_date','assigned_to']
        #exclude = [] --> will not show the fields which will included here
        widgets = {
            'title' : forms.TextInput(attrs={
                'class': "border-2 border-gray-300 w-full p-2 rounded-lg focus:border-rose-500 focus:ring-rose-500",
                'placeholder': "Enter task title"
            }),
            'description' : forms.Textarea(attrs={
                'class': "border-2 border-gray-300 w-full p-2 rounded-lg focus:border-rose-500 focus:ring-rose-500",
                'placeholder': "Describe the task"
            }),
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }