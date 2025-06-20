from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm, TaskForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('task_list')  # Redirect to task list page
    else:
        form = RegistrationForm()
    return render(request, 'register.jinja2', {'form': form})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the logged-in user
            task.save()
            return redirect('task_list')  # Redirect to the task list page
    else:
        form = TaskForm()
    return render(request, 'create_task.jinja2', {'form': form})

def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.jinja2', {'tasks': tasks})

def dashboard(request):
    today_tasks = Task.objects.filter(user=request.user, deadline__date=timezone.now().date())
    return render(request, 'dashboard.jinja2', {'today_tasks': today_tasks})
