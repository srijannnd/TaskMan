from django.shortcuts import render, redirect
from .models import Todo, ActivityFeed
from .forms import TodoForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def todo_list(request):
    obj = Todo.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            Todo.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                deadline=form.cleaned_data['deadline'],
            )
            ActivityFeed.objects.create(
                user=request.user,
                message='New Task Added'
            )
        return redirect('home')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_list.html', {'obj': obj, 'form': form})


@login_required
def del_todo(request, id):
    obj = Todo.objects.get(user=request.user, id=id).delete()
    ActivityFeed.objects.create(
        user=request.user,
        message='Task Deleted'
    )
    return redirect('home')


@login_required
def activity_feed(request):
    obj = ActivityFeed.objects.filter(user=request.user)
    return render(request, 'todo/todo_activity_feed.html', {'obj': obj})


def task_status(request, id):
    obj = Todo.objects.get(user=request.user, id=id)
    if obj.completed == True:
        obj.completed = False
    else:
        obj.completed = True
    obj.save()
    return redirect('home')