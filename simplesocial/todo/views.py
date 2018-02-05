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
            # deadline = form.cleaned_data['deadline']
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
        elif 'show-all' in request.POST:
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

    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoList2(APIView):

    def get_object(self, pk, user_id):
        try:
            return Todo.objects.get(pk=pk, user=user_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        todo = self.get_object(pk, user_id=request.user)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        todo = self.get_object(pk, user_id=request.user)
        todo.delete()
        return Response(status=status.HTTP_200_OK)

    # serializer = NotesSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

















