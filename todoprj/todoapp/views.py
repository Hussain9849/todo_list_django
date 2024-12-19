from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.contrib import messages

# Create your views here.
from .models import Todo


def base(request):
    return render(request, "base.html")

from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method=='POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        validate_user = authenticate(username=username,password=password)
        if validate_user is not None: #if user is not in database it returns None
            login(request,validate_user)# if user is in database it return not None(user)
            return redirect('todo_index')
        else:
            error_message = "login credentionals are incorrect please try again"
            return render(request,"login.html",{"error_message":error_message})
    return render(request, "login.html")

from django.contrib.auth.decorators import login_required
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            # Check if username is unique
            if User.objects.filter(username=username).exists():
                error_message = "User exists, use a different username"
                return render(request, 'register.html', {"error_message": error_message})
            try:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()
                return redirect('todo_index')
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                return render(request, 'register.html', {"error_message": error_message})
        else:
            error_message = "Passwords do not match!"
            return render(request, 'register.html', {"error_message": error_message})
    
    return render(request, 'register.html')

@login_required
def test_view(request):
    return HttpResponse("You are logged in!")



@login_required
def todo_index(request):
    print(f"User is_authenticated: {request.user.is_authenticated}")
    print(f"User logged in: {request.user.is_authenticated}")  # Debugging line
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = Todo(user=request.user,todo_name=task)
        new_todo.save()
    all_todos = Todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, "todo_index.html", context)

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('base')


from django.shortcuts import get_object_or_404

#@login_required
def complete_task(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.status = True  # Mark task as completed
    todo.save()
    return redirect('todo_index')

#@login_required
def delete_task(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()  # Delete the task
    return redirect('todo_index')
