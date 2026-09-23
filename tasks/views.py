from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Max,Min,Avg

# Create your views here.
def manager_dashboard(request):
    return render(request, 'dashboard/manager-dashboard.html')

def user_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')

def test(request):
    context = {
        "names": ["John", "Jane", "Doe"],
        "age": 30
    }
    return render(request, 'test.html', context)

def create_task(request):
    employees = Employee.objects.all()
    form = TaskModelForm() #for get

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():

            form.save()  # Save the form data to create a new Task instance
            return render(request, 'task_form.html', {'form': form, 'message': 'Task created successfully!'})

            """"for dajango form data"""
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to_ids = data.get('assigned_to')

            # task=Task.objects.create(
            #     title=title,
            #     description=description,
            #     due_date=due_date
            # )

            # # Assign the selected employees to the task
            # for emp_id in assigned_to_ids:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)

            # return HttpResponse("Task created successfully!")
            
    context = {"form": form}
    return render(request, 'task_form.html', context)

def view_task(request):

    # show the tasks which are completed
    # tasks = Task.objects.filter(status="COMPLETED")

    # show the tasks which are completed
    # tasks = Task.objects.filter(due_date=date.today())

    # tasks= TaskDetail.objects.exclude(priority="L")

    # show the tasks which are contain c and pending
    # tasks = Task.objects.filter(title__icontains="p",status="PENDING")

    # tasks = Task.objects.filter(Q(status="PENDING")| Q(status="IN_PROGRESS"))

    # tasks = Task.objects.all()
    # task3=Task.objects.get(id=1) 
    # first_task = Task.objects.first()

    # select related 
    # tasks = Task.objects.select_related('task').all()
    # tasks = TaskDetail.objects.select_related('task').all()
    # tasks = Task.objects.select_related('project').all()
    # tasks = Project.objects.select_related('task_set').all()

    # prefetch related 
    # tasks= Project.objects.prefetch_related('task_set').all()

    # tasks = Task.objects.prefetch_related('assigned_to').all()

    # task_count= Task.objects.aggregate(num_task=Count('id'))
    projects= Project.objects.annotate(num_task=Count('task')).order_by('num_task')

    return render(request ,"show_task.html",{"projects":projects})