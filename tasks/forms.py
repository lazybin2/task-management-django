from django import forms
from tasks.models import Task,TaskDetail

# dajango form for creating a new task
class TaskForm(forms.Form):
    title = forms.CharField(max_length=100, label='Task Title')
    description = forms.CharField(widget=forms.Textarea, label='Task Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget, label='Due Date')
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label='Assign To')

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees', [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]
        # You can customize the form fields here if needed

class StyledFormMixin:
    default_classes="border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-300 focus:ring-rose-300"
    def apply_styled_widgets(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder': f"Enter{field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder': f"Enter{field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':"border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-300 focus:ring-rose-300"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class':self.default_classes
                })

# django model form
class TaskModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets={
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }
        # exclude = ['Project','is_completed', 'created_at', 'updated_at']  # Exclude fields that should not be edited directly
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-300 focus:ring-rose-300", 'placeholder':"Enter task title"}),
        #     'description':forms.Textarea(attrs={'class': "border-4 border-gray-300 w-full rounded-lg shadow-sm focus:outline-none focus:border-rose-300 focus:ring-rose-300",'rows':5, 'placeholder':"Describe the task"}),
        #     'due_date': forms.SelectDateWidget(attrs={'class': "border-4 border-gray-300 rounded-lg shadow-sm focus:border-rose-300"}),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={'class': "border-4 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-300"}),
        #     }

    def __init__(self,*args,**kwarg):
        super().__init__(*args,**kwarg)
        self.apply_styled_widgets()

class TaskDetailModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority','notes']

    def __init__(self,*args,**kwarg):
            super().__init__(*args,**kwarg)
            self.apply_styled_widgets()
    