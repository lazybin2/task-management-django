from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm,TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Max,Min,Avg
from django.contrib import messages

# Create your views here.
def manager_dashboard(request):

    type=request.GET.get('type','all')

    # tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()
    

    # tasks= Task.objects.all()
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status="PENDING").count()

    # count = {
    #     'total_task': total_task,
    #     'completed_task': completed_task,
    #     'in_progress_task': in_progress_task,
    #     'pending_task': pending_task
    # }
    counts= Task.objects.aggregate(
        total=Count('id'),  
        completed=Count('id',filter=Q(status='COMPLETED')),
        in_progress=Count('id',filter=Q(status='IN_PROGRESS')),     
        pending=Count('id',filter=Q(status='PENDING'))      
    )

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    

    if type== 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type== 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type== 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type== 'all':
        tasks = base_query.all()

    contex = {
        'tasks':tasks,
        'counts':counts
        # 'total_task': total_task,
        # 'completed_task': completed_task,
        # 'in_progress_task': in_progress_task,
        # 'pending_task': pending_task
    }
    return render(request, 'dashboard/manager-dashboard.html',contex)

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
    task_form = TaskModelForm() #for get
    task_detail_form = TaskDetailModelForm() #for get

    if request.method == "POST":
        task_form = TaskModelForm(request.POST) 
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():

            task=task_form.save()  # Save the form data to create a new Task instance
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,"Task Created Successfully")
            return redirect('create-task')

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
            
    context = {"task_form": task_form, "task_detail_form":task_detail_form}
    return render(request, 'task_form.html', context)

def update_task(request,id):
    task=Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task) #for get

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details) #for get

    if request.method == "POST":
        task_form = TaskModelForm(request.POST,instance=task) 
        task_detail_form = TaskDetailModelForm(request.POST,instance=task)
        if task_form.is_valid() and task_detail_form.is_valid():

            task = task_form.save()  # Save the form data to create a new Task instance
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,"Task Updated Successfully")
            return redirect('create-task')

    context = {"task_form": task_form, "task_detail_form":task_detail_form}
    return render(request, 'task_form.html', context)

def delete_task(request,id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.success(request, 'Something is wrong')
        return redirect('manager-dashboard')

    


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