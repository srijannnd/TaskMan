from django.shortcuts import render, redirect
from .models import Todo, ActivityFeed
from .forms import TodoForm
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

# Create your views here.


@login_required
def todo_list(request):
    obj = Todo.objects.filter(user=request.user).order_by('-created_at')
    activities = ActivityFeed.objects.filter(user=request.user).order_by('-created_at')[:5]
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid() and form.cleaned_data['title']:
            deadline = form.cleaned_data['deadline']
            todo = Todo.objects.create(
                user=request.user,
                title=form.cleaned_data['title'].capitalize(),
                deadline=form.cleaned_data['deadline'],
            )
            ActivityFeed.objects.create(
                user=request.user,
                message='New Task "' + todo.title + '" Added'
            )
        elif 'show-completed' in request.POST:
            form = TodoForm()
            obj = Todo.objects.filter(user=request.user, completed=1).order_by('-created_at')
            return render(request, 'todo/todo_list.html', {'obj': obj, 'form': form, 'activities': activities})
        elif 'order-by-name' in request.POST:
            form = TodoForm()
            obj = Todo.objects.filter(user=request.user).order_by('title')
            return render(request, 'todo/todo_list.html', {'obj': obj, 'form': form, 'activities': activities})
        elif 'order-by-date' in request.POST:
            form = TodoForm()
            return render(request, 'todo/todo_list.html', {'obj': obj, 'form': form, 'activities': activities})
        else:
            list = request.POST
            for todo in obj:
                if str(todo.id) in list:
                    todo.completed = 1
                else:
                    todo.completed = 0
                todo.save()
        return redirect('home')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_list.html', {'obj': obj, 'form': form, 'activities': activities})


@login_required
def del_todo(request, id):
    obj = Todo.objects.get(user=request.user, id=id)
    ActivityFeed.objects.create(
        user=request.user,
        message='Task "' + obj.title.capitalize() + '" Deleted'
    )
    obj.delete()
    return redirect('home')


class TodoList(ListAPIView):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

