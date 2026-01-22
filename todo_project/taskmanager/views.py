from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
# Create your views here.

@login_required
def homePage(request):
    return render(request, 'home.html')

def signupPage(request):
    if request.method=="POST":
        full_name=request.POST.get('fullname')
        Username=request.POST.get('Username')
        Email=request.POST.get('Email')
        Password=request.POST.get('Password')
        Confirm_Password=request.POST.get('Confirm_Password')
        User_Types=request.POST.get('User_Types')

        user_exist=AuthUserModel.objects.filter(username=Username).exists()
        if user_exist:
            messages.warning(request, "USername Already exist")
            return redirect('signup')
        if Password==Confirm_Password:
            AuthUserModel.objects.create_user(
                full_name=full_name,
                username=Username,
                email=Email,
                password=Password,
                user_types=User_Types,
            )
            messages.success(request, "Account Created")
            return redirect('login')
        else:
            messages.warning(request, "Password Didnot Match")
            return redirect('signup')
    return render (request, 'auth/signup.html')

def loginPage(request):
    if request.method=="POST":
        Username=request.POST.get('Username')
        Password=request.POST.get('Password')

        user=authenticate(request, username=Username, password=Password)

        if user:
            login(request,user)
            messages.success(request, "Succesfully Login")
            return redirect ('home')
        else:
            messages.warning(request, 'Invalid Credentials')
            return redirect('login')

    return render (request, 'auth/login.html')

def logoutPage(request):
    logout(request)
    messages.success(request, "Succesfully Logout")
    return redirect('login')

@login_required
def changepassPage(request):
    C_user=request.user

    if request.method=="POST":
        Current_password=request.POST.get('Current_password')
        New_password=request.POST.get('New_password')
        Confirm_password=request.POST.get('Confirm_password')

        if check_password(Current_password,C_user.password):
            if New_password==Confirm_password:
                C_user.set_password(New_password)
                C_user.save()
                update_session_auth_hash(request,C_user)
                messages.success(request, "Succesfully Password Change")
                return redirect('home')
    return render (request, 'auth/changepass.html')

@login_required
def taskPage(request):
    user=request.user
    if user.user_types=="user":
        tasks=TaskModel.objects.filter(user=user)
    else:
        tasks=TaskModel.objects.all()
    return render(request, 'tasklist.html',{'tasks':tasks})
@login_required
def addtaskPage(request):
    if request.method=="POST":
        title=request.POST.get('title')
        Description=request.POST.get('Description')
        task_image=request.FILES.get('task_image')
        date=request.POST.get('date')
        status_types=request.POST.get('status_types')
        user=request.user

        TaskModel.objects.create(
            title=title,
            description=Description,
            due_date=date,
            task_image=task_image,
            status=status_types,
            user=user
        )
        messages.success(request, "Successfully Add Task")
        return redirect('task')
    return render(request, 'addtask.html')
@login_required
def edittaskPage(request, id):
    tasks=TaskModel.objects.get(id=id)
    if request.method=="POST":
        title=request.POST.get('title')
        Description=request.POST.get('Description')
        task_image=request.FILES.get('task_image')
        date=request.POST.get('date')
        status_types=request.POST.get('status_types')

        tasks.title=title
        tasks.description=Description
        if task_image:
            tasks.task_image=task_image
        tasks.due_date=date
        tasks.status=status_types

        tasks.save()
        messages.success(request, "Successfully Edit Task")
        return redirect('task')
    return render  (request, 'edittask.html',{'tasks':tasks} )
@login_required
def deletetaskPage(request, id):
    TaskModel.objects.get(id=id).delete()
    messages.success(request, "Successfully Task Delete")
    return redirect('task')
@login_required
def viewPage(request, id):
    tasks=TaskModel.objects.get(id=id)
    return render (request, 'view.html', {'tasks':tasks})

@login_required
def statusChange(request, id):
    tasks=TaskModel.objects.get(id=id)

    if tasks.status == "pending":
        tasks.status = 'Inprogress'
    elif tasks.status == "Inprogress":
        tasks.status = "Completed"
    tasks.save()
    return redirect('task')