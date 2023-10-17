from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from .forms import Data


def show_all_task(request):
    return render(request, 'task.html')


def create_task(request):
    if request.method == 'POST':
        data = Data(request.POST)
        if data.is_valid():
            # data fetching form the html form
            title = data.cleaned_data.get('title', None)
            description = data.cleaned_data.get('description', None)

            # save the data in database
            task = Task(title=title, description=description)
            task.save()
        return redirect(f'/work/user/')
    tasks = Task.objects.all()
    return render(request, 'task.html', {'tasks': tasks})


def delete_task(request, id):
    data = Task.objects.get(pk=id)
    data.delete()
    return redirect(f'/work/user/')


def update_task(request, id):
    task = Task.objects.get(pk=id)
    return render(request, 'update.html', {'task': task})


def do_update(request, id):
    if request.method == 'POST':
        data = Data(request.POST)
        if data.is_valid():
            title = data.cleaned_data.get('title', None)
            description = data.cleaned_data.get('description', None)

            task = Task.objects.get(pk=id)
            task.title = title
            task.description = description
            task.save()
    return redirect(f'/work/user/')


def complete_task(request, id):
    if request.method == 'POST':
        data = request.POST.get('toggle-button')
        task = Task.objects.get(pk=id)
        if (data == 'on'):
            task.status = True
        else:
            task.status = False
        task.save()
    return redirect(f'/work/user/')
