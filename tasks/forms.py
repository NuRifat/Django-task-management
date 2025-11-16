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

# Styled Form MIXINS
class StyledFormMixin:
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder' : f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder' : f"Enter {field.label.lower()}",
                    'rows' : 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })

# Django Model Form:
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        #fields = '__all__' #to bring all the fields from Task
        fields = ['title','description','due_date','assigned_to']
        #exclude = [] --> will not show the fields which will included here
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }
    
    def __init__(self,*arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()