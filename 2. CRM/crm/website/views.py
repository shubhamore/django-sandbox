from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
    records = Record.objects.all()
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('home')
    else:
        return render(request, 'home.html',{'records':records})
    
def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account was created for ' + username)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':record})
    else:
        messages.error(request, 'Please login first')
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, 'Record was deleted')
        return redirect('home')
    else:
        messages.error(request, 'Please login first')
        return redirect('home')
    
def add_record(request):
    form=AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=='POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record was added')
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.error(request, 'Please login first')
        return render(request, 'home.html', {'form':form})

def update_record(request,pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record was updated')
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.error(request, 'Please login first')
        return redirect('home')