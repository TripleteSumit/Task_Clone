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
            title = data.cleaned_data['title']
            description = data.cleaned_data['description']

            # save the data in database
            task = Task(title=title, description=description)
            task.save()
        return redirect(f'/work/user/')
    tasks = Task.objects.filter(status=False).all()
    return render(request, 'task.html', {'tasks': tasks})
