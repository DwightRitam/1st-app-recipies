from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def index(request):
    if request.method== "POST":
        data=request.POST
        receipe_name=data.get('receipe_name')
        receipe_desc=data.get('receipe_desc')
        reciepe_image=request.FILES.get('reciepe_image')
        
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_desc=receipe_desc,
            reciepe_image=reciepe_image,
        )
        return redirect('/reciepes')
    
    
    return render(request, 'index.html')

@login_required(login_url="/login")
def reciepes(request):
    queryset=Receipe.objects.all()

    if request.GET.get('search'):
        print(request.GET.get('search'))
        queryset=queryset.filter(receipe_name__icontains=request.GET.get('search'))
        
    context={"receipes": queryset}
    return render(request,'reciepes.html',context)

@login_required(login_url="/login")
def delete_reciepe(request,id):
    queryset=Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/reciepes')

@login_required(login_url="/login")
def update_reciepe(request,id):
    queryset=Receipe.objects.get(id=id)
    if request.method== "POST":
        data=request.POST
        receipe_name=data.get('receipe_name')
        receipe_desc=data.get('receipe_desc')
        reciepe_image=request.FILES.get('reciepe_image')
        
        #update all of them
        queryset.receipe_name=receipe_name
        queryset.receipe_desc=receipe_desc
        if reciepe_image:
            queryset.reciepe_image=reciepe_image
             
        queryset.save()
        
        return redirect('/reciepes')
    context={"receipe": queryset}
    return render(request,'update.html',context)

@login_required(login_url="/login")
def get_details(request,id):
    queryset=Receipe.objects.get(id=id)
    # queryset=Receipe.objects.all()
    context={"details": queryset}
    
    return render(request,'details.html',context)
    

def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login')
        
        user=authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login')
        
        else:
            login(request,user)
            return redirect('/')
            
    return render(request,'login.html')

def sign(request):
    if request.method=="POST":
        
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user =User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username already exists')
            return redirect('/sign')
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        
        user.set_password(password) 
        user.save()
        login(request,user)
        return redirect('/')
    
    return render(request,'sign.html')

def logout_page(request):
    logout(request)
    return redirect('/login')