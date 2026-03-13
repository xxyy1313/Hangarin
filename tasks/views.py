from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Task
from .forms import TaskForm


def dashboard(request):
    tasks = Task.objects.all().order_by('-created_at')[:5]
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status='Pending').count()
    in_progress_tasks = Task.objects.filter(status='In Progress').count()
    completed_tasks = Task.objects.filter(status='Completed').count()

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'tasks/dashboard.html', context)


def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')

    search_query = request.GET.get('q')
    status = request.GET.get('status')
    category = request.GET.get('category')
    priority = request.GET.get('priority')

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if status:
        tasks = tasks.filter(status=status)

    if category:
        tasks = tasks.filter(category__id=category)

    if priority:
        tasks = tasks.filter(priority__id=priority)

    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks/task_list.html', context)


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'page_title': 'Add Task'})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'page_title': 'Edit Task'})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})